import numpy as np
from Task3.element import HospitalElement


class HospitalCreate(HospitalElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outAct(self):
        super().outAct()
        self.tnext[0] = self.tcurr + super().getDelay()
        self.next_patientType = np.random.choice([1, 2, 3], p=[0.5, 0.1, 0.4])
        nextEl = self.get_next_element()
        nextEl.inAct(self.next_patientType, self.tcurr)
