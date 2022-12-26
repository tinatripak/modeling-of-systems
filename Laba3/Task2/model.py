import numpy as np
from Task2.calculation import get_mean_departure_time, get_mean_bank_time, get_mean_client, get_result
from Task1.model import Model
from Task2.process import BankProcess


class BankModel(Model):
    def __init__(self, elements, items=None):
        super().__init__(elements)
        self.items = items
        self.lane_changes_count = 0
        self.meanClient = 0

    def simulate(self, timeModeling):
        while self.tcurr < timeModeling:
            self.tnext = float('inf')
            for item in self.list:
                tnextValue = np.min(item.tnext)
                if tnextValue < self.tnext:
                    self.tnext = tnextValue
                    self.event = item.id
            for item in self.list:
                item.doStatistics(self.tnext - self.tcurr)
            self.change_count_meanClient(self.tnext - self.tcurr)
            self.tcurr = self.tnext
            for item in self.list:
                item.tcurr = self.tcurr
            if len(self.list) > self.event:
                self.list[self.event].outAct()
            for item in self.list:
                if self.tcurr in item.tnext:
                    item.outAct()
            self.change_queue()
        
        self.printResult()
        return self.printTotalResult()

    def change_count_meanClient(self, delta):
        states_count = self.items[0].state[0] + self.items[1].state[0]
        queue_count = self.items[0].queue + self.items[1].queue
        self.meanClient += (queue_count + states_count) * delta

    def change_queue(self):
        queue_elements = self.get_queue()
        firstItem = queue_elements[0] - queue_elements[1]
        secondItem = queue_elements[1] - queue_elements[0]

        if firstItem >= 2:
            self.list[1].queue -= 1
            self.list[2].queue += 1
            self.lane_changes_count += 1

            print("Змінити перше віконце банку на друге")

        elif secondItem >= 2:
            self.list[2].queue -= 1
            self.list[1].queue += 1
            self.lane_changes_count += 1

            print("Змінити друге віконце банку на перше")

    def get_queue(self):
        queue_elements = list()
        for e in self.list:
            isBank = isinstance(e, BankProcess)
            if isBank:
                queue_elements.append(e.queue)

        return queue_elements

    def printResult(self):
        super().printResult()

        for e in self.list:
            e.printResult()
            isBank = isinstance(e, BankProcess)
            if isBank:
                print(f'Cередній інтервал часу між відїздами клієнтів від вікон = {get_mean_departure_time(e)}')

    def printTotalResult(self):
        super().printTotalResult()
        processors_count = 0
        timeBank_sum = 0
        timeDeparture_sum = 0

        for e in self.list:
            e.printResult()
            isBank = isinstance(e, BankProcess)
            if isBank:
                timeDeparture_sum += get_mean_departure_time(e)
                timeBank_sum += get_mean_bank_time(e)
                processors_count += 1

        time_departure_res = get_result(timeDeparture_sum, processors_count)
        time_bank_res = get_result(timeBank_sum, processors_count)

        print(f"Середній інтервал часу між від'їздами клієнтів від вікон : {time_departure_res}\n" +
              f"Середній час в банку: {time_bank_res}\n" +
              f"Середня кількість клієнтів в банку: {get_mean_client(self.meanClient, self.tcurr)}\n" +
              f"Кількість змін підїзних смуг : {self.lane_changes_count}\n")

        return {
            "time_departure_res": time_departure_res,
            "time_bank_res": time_bank_res
        }
