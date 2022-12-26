import distributions
import numpy as np


class Element:
    nextId = 0
    arr = [1]

    def __init__(self,
            name=None,
            delayMean=1.,
            delayDev=0.,
            distribution='',
            probability=1,
            channels=1,
            maxqueue=float('inf')):

        self.tnext = [0] * channels 
        self.delayMean = delayMean
        self.delayDev = delayDev 
        self.quantity = 0
        self.tcurr = 0 
        self.state = [0] * channels
        self.nextElement = None
        
        self.id = Element.nextId
        Element.nextId += 1

        self.distribution = distribution

        if name is None:
            self.name = 'element' + str(self.id)
        else:
            self.name = name
        
        self.probability = [probability]
        self.priorities = Element.arr

        self.queue = 0
        self.maxqueue = maxqueue
        self.meanqueue = 0.0
        self.channels = channels
        self.meanload = 0
        self.failure = 0

    def get_state(self):
        return self.state

    def set_state(self, value):
        self.state = value

    def get_tnext(self):
        return self.tnext

    def set_tnext(self, value):
        self.tnext = value

    def get_tcurr(self):
        return self.tcurr

    def set_tcurr(self, value):
        self.tcurr = value

    def get_next_element(self):
        isPriority = self.priorities == Element.arr 
        isProbability = Element.arr == self.probability

        if isPriority:
            return np.random.choice(a=self.nextElement, p=self.probability)
        elif isProbability:
            return self.get_from_priority()
        elif isPriority and isProbability:
            return self.nextElement[0]
        elif not isPriority and not isProbability:
            raise Exception('Помилка отримання наступного елемента')

    def get_from_priority(self):
        index = 0
        min_queue = float('inf')
        priorities = self.priorities.copy()

        for i in range(len(priorities)):
            maximum_priority = max(priorities)
            if maximum_priority == -1:
                break
            maximum_priority_index = priorities.index(maximum_priority)
            if 0 in self.nextElement[maximum_priority_index].state:
                return self.nextElement[maximum_priority_index]
            else:
                if self.nextElement[maximum_priority_index].queue < min_queue:
                    min_queue = self.nextElement[maximum_priority_index].queue
                    index = self.nextElement.index(self.nextElement[maximum_priority_index])
            priorities[maximum_priority_index] = -1

        return self.nextElement[index]

    def getDelay(self):
        if 'exp' == self.distribution:
            return distributions.exponential_distribution(self.delayMean)
        elif 'norm' == self.distribution:
            return distributions.normal_distribution(self.delayMean, self.delayDev)
        elif 'unif' == self.distribution:
            return distributions.uniform_distribution(self.delayMean, self.delayDev)
        elif 'erlang' == self.distribution:
            return distributions.erlang_distribution(self.delayMean, self.delayDev)
        else:
            return self.delayMean

    def inAct(self):
        pass

    def outAct(self):
        self.quantity += 1

    def doStatistics(self, delta):
        self.meanqueue += self.queue * delta
        for i in range(self.channels):
            self.meanload += self.state[i] * delta
        self.meanload = self.meanload / self.channels

    def getAvailable(self):
        availableChannels = []
        for i in range(self.channels):
            if self.state[i] == 0:
                availableChannels.append(i)

        return availableChannels

    def getCurrent(self):
        currentChannels = []
        for i in range(self.channels):
            if self.tnext[i] == self.tcurr:
                currentChannels.append(i)
        return currentChannels

    def printResult(self):
        print(f'{self.name} кількість = {str(self.quantity)} статус = {self.state}')

    def printInfo(self):
        print(f'{self.name} кількість = {self.quantity} статус = {self.state} tnext = {self.tnext}')

