import Distributions.distributions as distributions
import numpy as np


class Element:
    next_id = 0
    arr = [1]

    def __init__(self,
            name=None,
            delayMean=1.,
            delayDev=0.,
            distribution='',
            probability=1,
            channels=1,
            maxqueue=float('inf')):

        self.name = 'element' + str(self.id) if name is None else name
        self.delayMean = delayMean
        self.delayDev = delayDev
        self.distribution = distribution
        self.probability = [probability]
        self.tnext = [0] * channels
        self.state = [0] * channels
        self.channels = channels
        self.maxqueue = maxqueue

        self.quantity = 0
        self.tcurr = 0
        self.queue = 0
        self.meanqueue = 0.0
        self.meanload = 0
        self.failure = 0
        self.nextElement = None
        self.id = Element.next_id
        Element.next_id += 1
        self.priorities = Element.arr

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
        isProbability = self.probability == Element.arr

        if not isProbability and not isPriority:
            raise Exception('Помилка отримання наступного елементу')
        elif isPriority:
            return np.random.choice(a=self.nextElement, p=self.probability)
        elif isProbability:
            return self.get_from_priority()
        elif isProbability and isPriority:
            return self.nextElement[0]

    def get_from_priority(self):
        min_index_queue = 0
        min_element_queue = float('inf')
        copy_priorities = self.priorities.copy()

        for i in range(len(copy_priorities)):
            max_priority = max(copy_priorities)
            if max_priority == -1:
                break

            index_maxPriority = copy_priorities.index(max_priority)
            if 0 in self.nextElement[index_maxPriority].state:
                return self.nextElement[index_maxPriority]
            else:
                if self.nextElement[index_maxPriority].queue < min_element_queue:
                    min_element_queue = self.nextElement[index_maxPriority].queue
                    min_index_queue = self.nextElement.index(self.nextElement[index_maxPriority])
            copy_priorities[index_maxPriority] = -1

        return self.nextElement[min_index_queue]

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
