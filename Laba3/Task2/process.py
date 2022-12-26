import numpy as np
from element import Element


class BankProcess(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bank_meanTime = 0
        self.bank_prevTime = 0
        self.departure_meanTime = 0
        self.departure_prevTime = 0

        self.tnext = [np.inf] * self.channels
        self.state = [0] * self.channels

    def inAct(self):        
        availableChannels = self.getAvailable()
        if len(availableChannels) > 0:
            for i in availableChannels:
                self.bank_prevTime = self.tcurr
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                break
        else:
            if self.queue < self.maxqueue:
                self.queue += 1
            else:
                self.failure += 1

    def outAct(self):
        super().outAct()
        currentChannels = self.getCurrent()
        for i in currentChannels:
            self.tnext[i] = np.inf
            self.state[i] = 0
            self.departure_meanTime += self.tcurr - self.departure_prevTime
            self.departure_prevTime = self.tcurr
            self.bank_meanTime = + self.tcurr - self.bank_prevTime
            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
            if self.nextElement is not None:
                nextElement = self.get_next_element()
                nextElement.inAct()