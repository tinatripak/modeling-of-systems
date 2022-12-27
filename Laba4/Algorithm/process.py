import numpy as np
from Algorithm.element import Element


class Process(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tnext = [np.inf] * self.channels
        self.state = [0] * self.channels

    def inAct(self):        
        availableChannels = self.getAvailable()
        if len(availableChannels) > 0:
            for i in availableChannels:
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                break
        else:
            if self.queue < self.maxqueue:
                self.queue += 1
            else:
                self.failure += 1

    def outAct(self):
        currentChannels = self.getCurrent()
        for i in currentChannels:
            super().outAct()
            self.tnext[i] = np.inf
            self.state[i] = 0
            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.tnext[i] = self.tcurr + self.getDelay()
            if self.nextElement is not None:
                nextElement = self.get_next_element()
                nextElement.inAct()