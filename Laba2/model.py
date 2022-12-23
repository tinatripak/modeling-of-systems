import numpy as np
from process import Process

class Model:
    def __init__(self, elements):
        self.list = elements
        self.tnext = 0.0
        self.event = 0
        self.tcurr = self.tnext

    def simulate(self, time):
        while self.tcurr < time:
            self.tnext = float('inf')
            for e in self.list:
                tnextValue = np.min(e.tnext)
                if tnextValue < self.tnext:
                    self.tnext = tnextValue
                    self.event = e.id

            for e in self.list:
                e.doStatistics(self.tnext - self.tcurr)

            self.tcurr = self.tnext

            for e in self.list:
                e.tcurr = self.tcurr

            if len(self.list) > self.event:
                self.list[self.event].outAct()

            for e in self.list:
                if self.tcurr in e.tnext:
                    e.outAct()

            for e in self.list:
                e.printInfo()

        self.printResult()
        
        return self.printTotalResult()

    def get_failure(self, e: Process):
        return e.failure / (e.quantity + e.failure) if (e.quantity + e.failure) != 0 else 0
    
    def get_meanload(self, e: Process):
        return e.meanload / self.tcurr
    
    def get_meanqueue(self, e: Process):
        return e.meanqueue / self.tcurr

    def printResult(self):
        print('\nРезультати:')

        for e in self.list:
            e.printResult()
            if isinstance(e, Process):
                print(f"Середня довжина черги: {self.get_meanqueue(e)}\n"+
                    f"Імовірність відмови: {self.get_failure(e)}\n"+
                    f"Середнє навантаження: {self.get_meanload(e)}\n")


    def printTotalResult(self):
        print('\nЗагальні результати:')

        failure_sum = 0
        meanload_sum = 0
        meanqueue_sum = 0
        processors_count = 0

        for e in self.list:
            if isinstance(e, Process):
                processors_count += 1
                failure_sum += self.get_failure(e)
                meanload_sum += self.get_meanload(e)
                meanqueue_sum += self.get_meanqueue(e)

        failure_res = failure_sum / processors_count
        meanload_res = meanload_sum / processors_count
        meanqueue_res = meanqueue_sum / processors_count

        print(f"Середня довжина черги: {meanqueue_res}\n" +
              f"Імовірність відмови: {failure_res} \n" +
              f"Середнє навантаження: {meanload_res}\n")

        return {
            "meanqueue_res": meanqueue_res,
            "failure_res": failure_res,
            "meanload_res": meanload_res
        }
