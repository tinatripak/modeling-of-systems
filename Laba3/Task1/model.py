import numpy as np
from Task1.calculation import get_failure_probability, get_meanload, get_meanqueue_len, get_result
from Task1.process import Process
from Task2.process import BankProcess
from Task3.process import HospitalProcess


class Model:
    def __init__(self, elements):
        self.list = elements
        self.event = 0
        self.tnext = 0.0
        self.tcurr = self.tnext

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
            self.tcurr = self.tnext
            for item in self.list:
                item.tcurr = self.tcurr
            if len(self.list) > self.event:
                self.list[self.event].outAct()
            for item in self.list:
                if self.tcurr in item.tnext:
                    item.outAct()

        self.printResult()
        return self.printTotalResult()

    def printResult(self):
        print('\nРезультати')
        for e in self.list:
            e.printResult()
            if isinstance(e, Process) or isinstance(e, BankProcess) or isinstance(e, HospitalProcess):
                print(f"Середня довжина черги: {get_meanqueue_len(e, self.tcurr)}\n" +
                      f"Імовірність відмови: {get_failure_probability(e)}\n" +
                      f"Середнє навантаження: {get_meanload(e, self.tcurr)}\n")

    def printTotalResult(self):
        meanload_sum = 0
        meanqueue_length_sum = 0
        failure_probability_sum = 0
        processors_count = 0

        print('\nЗагальні результати')
        for e in self.list:
            if isinstance(e, Process) or isinstance(e, BankProcess) or isinstance(e, HospitalProcess):
                meanload_sum += get_meanload(e, self.tcurr)
                meanqueue_length_sum += get_meanqueue_len(e, self.tcurr)
                failure_probability_sum += get_failure_probability(e)
                processors_count += 1

        meanqueue_len_result = get_result(meanqueue_length_sum, processors_count)
        failure_probability_result = get_result(failure_probability_sum, processors_count)
        meanload_result = get_result(meanload_sum, processors_count)

        print(f"Середня довжина черги: {meanqueue_len_result}\n" +
              f"Імовірність відмови: {failure_probability_result}\n" +
              f"Середнє навантаження: {meanload_result}\n")

        return {
            "meanqueue_len_result": meanqueue_len_result,
            "failure_probability_result": failure_probability_result,
            "meanload_result": meanload_result
        }

    