import numpy as np
from Task3.element import HospitalElement
from Task3.calculation import get_division_result


class HospitalProcess(HospitalElement):
    def __init__(self, 
            path=None, 
            **kwargs):
        super().__init__(**kwargs)
        self.path = path

        self.time_to_laboratory = 0
        self.tprevTime_to_laboratory = 0
        self.second_type_patient_finished_time = 0
        self.second_type_patient_count = 0

        self.patient_types = [-1] * self.channels
        self.time_starts = [-1] * self.channels

        self.arr_patient_types = []
        self.arr_priority = []
        self.arr_time_starts = []

    def get_priority_i(self):
        for i in self.patient_types:
            for j in np.unique(self.arr_patient_types):
                if j == i:
                    return self.arr_patient_types.index(j)
        else:
            return 0

    def inAct(self, next_patientType, startTime):
        self.next_patientType = next_patientType

        if self.name == 'Шлях в реєстратуру лабораторії':
            self.time_to_laboratory += self.tcurr - self.tprevTime_to_laboratory
            self.tprevTime_to_laboratory = self.tcurr

        if next_patientType == 2 and self.name == 'Шлях в реєстратуру':
            self.second_type_patient_finished_time += self.tcurr - startTime
            self.second_type_patient_count += 1

        availableChannels = self.getAvailable()
        if len(availableChannels) > 0:
            for i in availableChannels:
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                self.patient_types[i] = self.next_patientType
                self.time_starts[i] = startTime
                break
        else:
            if self.maxqueue > self.queue:
                self.queue += 1
                self.arr_patient_types.append(self.next_patientType)
                self.arr_time_starts.append(startTime)
            else:
                self.failure += 1

    def outAct(self):
        super().outAct()
        currentChannels = self.getCurrent()
        for i in currentChannels:
            self.tnext[i] = np.inf
            self.state[i] = 0
            prev_patient_type = self.patient_types[i]
            prev_startTime = self.time_starts[i]
            self.patient_types[i] = -1
            self.time_starts[i] = -1

            if self.queue > 0:
                self.queue -= 1
                priority_i = self.get_priority_i()
                self.next_patientType = self.arr_patient_types.pop(priority_i)
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                self.patient_types[i] = self.next_patientType
                self.time_starts[i] = self.arr_time_starts.pop(priority_i)

            if self.nextElement is not None:
                if self.name == 'Шлях в реєстратуру':
                    self.next_patientType = 1
                else:
                    self.next_patientType = prev_patient_type

                if self.path is None:
                    next_el = np.random.choice(self.nextElement, p=self.probability)
                    next_el.inAct(self.next_patientType, prev_startTime)
                else:
                    for index, path in enumerate(self.path):
                        if self.next_patientType in path:
                            next_el = self.nextElement[index]
                            next_el.inAct(self.next_patientType, prev_startTime)
                            break

    def get_meanTime_for_secondType(self):
        if self.second_type_patient_count != 0:
            return get_division_result(self.second_type_patient_finished_time, self.second_type_patient_count)
        else:
            return np.inf

    def doStatistics(self, delta):
        self.meanqueue_length = + delta * self.queue

    def printInfo(self):
        super().printInfo()
        print(f'черга={self.queue}, невдача={self.failure}')
        print(f'Типи пацієнтів={self.patient_types}')
