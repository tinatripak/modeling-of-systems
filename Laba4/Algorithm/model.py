import numpy as np
from Algorithm.process import Process


class Model:
    def __init__(self, elements):
        self.list = elements
        self.event = 0
        self.tnext = 0.0
        self.tcurr = self.tnext

    def simulate(self, timeModeling):
        while self.tcurr < timeModeling:
            self.tnext = float('inf')
            for e in self.list:
                tnext_val = np.min(e.tnext)
                if tnext_val < self.tnext:
                    self.tnext = tnext_val
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
    
    def get_meanload(self, e: Process):
        return e.meanload / self.tcurr