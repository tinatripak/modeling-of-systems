import numpy as np
from Task3.calculation import get_division_result
from Task3.exitElement import HospitalExit
from Task3.process import HospitalProcess
from Task1.model import Model


class HospitalModal(Model):
    def __init__(self, elements: list):
        super().__init__(elements)
        self.event = elements[0]

    def get_filtered_elements(self, function):
        return filter(function, self.list)

    def simulate(self, timeModeling):
        while self.tcurr < timeModeling:
            self.tnext = float('inf')
            filtered_array = self.get_filtered_elements(lambda e: not isinstance(e, HospitalExit))
            for e in filtered_array:
                tnext_val = np.min(e.tnext)
                if tnext_val < self.tnext:
                    self.tnext = tnext_val
                    self.event = e.id
            for e in self.list:
                e.doStatistics(self.tnext - self.tcurr)
            self.tcurr = self.tnext
            for e in self.list:
                e.tcurr = self.tcurr
            for e in self.list:
                if self.tcurr in e.tnext:
                    e.outAct()

        self.printResult()
        return self.printTotalResult()

    def printResult(self):
        super().printResult()
        hospitalExits = self.get_filtered_elements(lambda e: isinstance(e, HospitalExit))
        hospitalProcesses = self.get_filtered_elements(lambda e: isinstance(e, HospitalProcess))
        notProcessesNotExits = self.get_filtered_elements(lambda e: not isinstance(e, HospitalExit) and not isinstance(e, HospitalProcess))

        process: HospitalProcess
        print('Лікарняні процеси')
        for process in hospitalProcesses:
            if process.name == 'Шлях в реєстратуру':
                    print(
                        f'Середній час завершення - тип 2 = {process.get_meanTime_for_secondType()}')

        exit: HospitalExit
        print('Закінчення')
        for exit in hospitalExits:
            print(f'Середній час завершення - тип 1 = {exit.get_average_finished_time(1)}\n' +
                  f'Середній час завершення - тип 2 = {exit.get_average_finished_time(2)}\n' +
                  f'Середній час завершення - тип 3 = {exit.get_average_finished_time(3)}\n')

        print('Інші процеси')
        for e in notProcessesNotExits:
            e.printResult()

    def printTotalResult(self):
        super().printTotalResult()
        processors_count = 0
        intervalTime_sum = 0
        finishedTime_sum = 0
        finished_count = 0
        hospitalProcesses = self.get_filtered_elements(lambda e: isinstance(e, HospitalProcess))
        hospitalExits = self.get_filtered_elements(lambda e: isinstance(e, HospitalExit))

        process: HospitalProcess
        # print('Лікарняні процеси')
        for process in hospitalProcesses:
            processors_count += 1
            if process.name == 'Шлях в реєстратуру лабораторії':
                intervalTime_sum += get_division_result(process.time_to_laboratory, process.quantity)
        
        exit: HospitalExit
        # print('Закінчення')
        for exit in hospitalExits:
            finishedTime_sum += sum(exit.arr_finishTimes)
            finished_count += exit.quantity

        intervalTime_mean = intervalTime_sum
        finished_time_mean = get_division_result(finishedTime_sum, finished_count)

        print(f'Середній час, проведений хворим у системі: {intervalTime_mean}\n' +
              f'Середній час завершення: {finished_time_mean}\n')
