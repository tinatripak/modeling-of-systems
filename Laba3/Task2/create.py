from element import Element


class BankCreate(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outAct(self):
        super().outAct()
        self.tnext[0] = self.tcurr + super().getDelay()
        firstElement = self.nextElement[0]
        secondElement = self.nextElement[1]

        ifEqual = firstElement.queue == secondElement.queue
        ifEqualTwoCondition = firstElement.queue == 0 and secondElement.queue == 0
        ifsecondElementMore = firstElement.queue < secondElement.queue

        if ifEqual or ifEqualTwoCondition or ifsecondElementMore:
            firstElement.inAct()
        else:
            secondElement.inAct()
