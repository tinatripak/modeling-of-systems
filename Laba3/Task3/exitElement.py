import numpy as np
from Task3.element import HospitalElement


class HospitalExit(HospitalElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.arr_finishTimes = [0, 0, 0]
        self.patientType_score = [0, 0, 0]

        self.tnext = [np.inf]

    def inAct(self, type, startTime):
        i = type - 1

        self.arr_finishTimes[i] += self.tcurr - startTime
        self.patientType_score[i] += 1
        super().outAct()

    def get_average_finished_time(self, patient_type):
        i = patient_type - 1
        
        count = self.patientType_score[i]
        if count != 0:
            return self.arr_finishTimes[i] / count
        else:
            return np.inf
