import distributions

class Element:
    staticNextId = 0

    def __init__(self, delay=None, distribution=None):
        self.id = Element.staticNextId
        Element.staticNextId += 1
        self.name = 'element' + str(self.id)
        self.tnext = [0]
        self.delayMean = delay
        self.delayDev = None
        self.distribution = distribution
        self.quantity = 0
        self.tcurr = self.tnext
        self.state = [0]
        self.nextElement = None
        self.probability = [1]


    def getDelay(self):
        if 'exp' == self.distribution:
            return distributions.exponential_distribution(self.delayMean)
        elif 'norm' == self.distribution:
            return distributions.normal_distribution(self.delayMean, self.delayDev)
        elif 'unif' == self.distribution:
            return distributions.uniform_distribution(self.delayMean, self.delayDev)
        else:
            return self.delayMean

    def get_tcurr(self):
        return self.tcurr

    def set_tcurr(self, value):
        self.tcurr = value

    def get_state(self):
        return self.state

    def set_state(self, value):
        self.state = value
    
    def get_tnext(self):
        return self.tnext

    def set_tnext(self, value):
        self.tnext = value

    def inAct(self):
        pass

    def outAct(self):
        self.quantity += 1

    def printResult(self):
        print(f'{self.name} кількість = {str(self.quantity)} стан = {self.state}')

    def printInfo(self):
        print(f'{self.name} стан = {self.state} кількість = {self.quantity} затримка наступного елементу = {self.tnext}')

    def doStatistics(self, delta):
        pass
