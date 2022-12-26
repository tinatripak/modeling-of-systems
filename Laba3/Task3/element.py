from element import Element


class HospitalElement(Element):
    delayMean_dict = { 1: 15, 2: 40, 3: 30 }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_patientType = None

    def getDelay(self):
        if self.name == 'Реєстратура':
            self.delayMean = HospitalElement.delayMean_dict[self.next_patientType]
        return super().getDelay()

    def inAct(self, next_patientType, startTime):
        pass
