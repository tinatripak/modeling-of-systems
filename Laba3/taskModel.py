import distributions

from Task1.create import Create
from Task1.model import Model
from Task1.process import Process

from Task2.create import BankCreate
from Task2.model import BankModel
from Task2.process import BankProcess

from Task3.create import HospitalCreate
from Task3.model import HospitalModal
from Task3.process import HospitalProcess
from Task3.exitElement import HospitalExit

class TaskModel():
    def get_model_with_multichannel_service(self):
        creator = Create(
            delayMean=7, 
            name='Створювач', 
            distribution='exp')

        first_process = Process(
            maxqueue=8, 
            channels=4, 
            delayMean=7, 
            distribution='exp')

        creator.nextElement = [first_process]
        elements = [creator, first_process]
        model = Model(elements)
        model.simulate(1000)
    
    def get_model_with_priority_route_selection(self):
        first_process = Process(
            maxqueue=3, 
            name='Таска 1', 
            delayMean=6, 
            distribution='exp')

        first_process.priorities = [1, 2]

        creator = Create(
            delayMean=6, 
            name='Створювач', 
            distribution='exp')

        second_process = Process(
            maxqueue=3, 
            name='Таска 2', 
            delayMean=6, 
            distribution='exp')

        third_process = Process(
            maxqueue=3, 
            name='Таска 3', 
            delayMean=6, 
            distribution='exp')

        creator.nextElement = [first_process]
        first_process.nextElement = [second_process, third_process]

        elements = [creator, first_process, second_process, third_process]
        model = Model(elements)
        model.simulate(1000)

    def get_model_with_given_probability(self):
        first_process = Process(
            maxqueue=3, 
            delayMean=6, 
            distribution='exp')

        first_process.probability = [0.6, 0.4]
        creator = Create(
            delayMean=6, 
            name='Створювач', 
            distribution='exp')

        second_process = Process(
            maxqueue=3, 
            delayMean=6, 
            distribution='exp')

        third_process = Process(
            maxqueue=3, 
            delayMean=6, 
            distribution='exp')

        creator.nextElement = [first_process]
        first_process.nextElement = [second_process, third_process]

        elements = [creator, first_process, second_process, third_process]
        model = Model(elements)
        model.simulate(1000)

    def get_bank_model(self):
        creator = BankCreate(
            delayMean=0.6, 
            name='Створювач банку', 
            distribution='exp')

        first_process = BankProcess(
            maxqueue=3, 
            delayMean=0.3, 
            name='Перша каса', 
            distribution='exp')

        second_process = BankProcess(
            maxqueue=3, 
            delayMean=0.3, 
            name='Друга каса', 
            distribution='exp')

        creator.nextElement = [first_process, second_process]

        first_process.state[0] = 1
        second_process.state[0] = 1

        first_process.tnext[0] = distributions.normal_distribution(1, 0.3)
        second_process.tnext[0] = distributions.normal_distribution(1, 0.3)

        creator.tnext[0] = 0.1

        first_process.queue = 2
        second_process.queue = 2

        element_list = [creator, first_process, second_process]
        bank = BankModel(element_list, items=[first_process, second_process])
        bank.simulate(1000)

    def get_hospital_model(self):
        creator = HospitalCreate(
            delayMean=15.0, 
            name='Створювач лікарні', 
            distribution='exp')

        registration = HospitalProcess(
            maxqueue=90,
            channels=2,
            name='Реєстратура',
            distribution='exp')

        ward = HospitalProcess(
            maxqueue=90,
            delayMean=3.0, 
            delayDev=8,
            channels=3,
            name='Шлях в палату',
            distribution='unif')

        laboratory_registry = HospitalProcess(
            maxqueue=0,
            delayMean=2.0,
            delayDev=5,
            channels=10,
            name='Шлях в реєстратуру лабораторії',
            distribution='unif')

        taking_tests = HospitalProcess(
            maxqueue=90,
            delayMean=4.5,
            delayDev=3,
            channels=1,
            name='Шлях в лабораторію на здачу аналізів',
            distribution='erlang')

        verification_analyses = HospitalProcess(
            maxqueue=90,
            delayMean=4.0,
            delayDev=2,
            channels=1,
            name='Перевірка аналізів',
            distribution='erlang')

        registry = HospitalProcess(
            maxqueue=0,
            delayMean=2.0,
            delayDev=5,
            channels=10,
            name='Шлях в реєстратуру',
            distribution='unif')

        first_exit = HospitalExit(name='Перший вихід')
        second_exit = HospitalExit(name='Другий вихід')

        creator.nextElement = [registration]
        registration.nextElement = [ward, laboratory_registry]
        ward.nextElement = [first_exit]
        laboratory_registry.nextElement = [taking_tests]
        taking_tests.nextElement = [verification_analyses]
        verification_analyses.nextElement = [second_exit, registry]
        registry.nextElement = [registration]

        registration.priorities = [1]
        registration.path = [[1], [2, 3]]
        verification_analyses.path = [[3], [2]]

        model = HospitalModal([creator, registration, ward, laboratory_registry, 
        taking_tests, verification_analyses, registry, first_exit, second_exit])
        model.simulate(1000)
