import random
from Algorithm.create import Create
from Algorithm.model import Model
from Algorithm.process import Process

def get_delayMean():
    return random.randint(1, 5)

def create_mass_service_model(number_systems):
    creator = Create(
        delayMean=get_delayMean(), 
        name='Створювач', 
        distribution='exp')

    elements = [creator]
    for i in range(number_systems):

        process = Process(
            delayMean=get_delayMean(), 
            name=f'Process {i + 1}', 
            distribution='exp')

        elements[i].nextElement = [process]
        elements.append(process)

    model = Model(elements)
    return model

def create_system(number_systems):
    i = 0

    creator = Create(
        delayMean=get_delayMean(), 
        name='Створювач', 
        distribution='exp')

    elements = [creator]

    while i < number_systems:
        first_process = Process(
            delayMean=get_delayMean(), 
            name=f'Process {i + 1}', 
            distribution='exp')
        elements[i].nextElement = [first_process]

        second_process = Process(
            delayMean=get_delayMean(), 
            name=f'Process {i + 2}', 
            distribution='exp')

        third_process = Process(
            delayMean=get_delayMean(), 
            name=f'Process {i + 3}', 
            distribution='exp')

        first_process.probability = [0.3, 0.7]
        first_process.nextElement = [second_process, third_process]
        
        fourth_process = Process(
            delayMean=get_delayMean(), 
            name=f'Process {i + 4}', 
            distribution='exp')

        second_process.nextElement = [fourth_process]
        third_process.nextElement = [fourth_process]
        
        i += 4

        processes = [first_process, second_process, third_process, fourth_process]
        for p in processes:
            elements.append(p)

    model = Model(elements)
    return model