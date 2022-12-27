import time
import matplotlib.pyplot as plt
from Algorithm.element import Element
from Algorithm.model import Model
from Algorithm.process import Process

timeModeling = 1000

def analyze_theoretical(model: Model, timeModeling: int = timeModeling):
    intencity = 0
    model.list: list[Element]

    for e in model.list:
        ifProcess = isinstance(e, Process)
        if ifProcess:
            intencity += model.get_meanload(e) / model.tcurr

    return 2 * timeModeling * intencity

def analyze(create_model, events_count):
    execution_time = []
    experiments_count = 3
    theoretical_values = []

    for i in events_count:
        theoretical_sum = 0
        execution_time_sum = 0

        for j in range(experiments_count):
            model = create_model(i)
            print(f'Кількість подій в моделі {i}, експеримент №{j+1}')
            start = time.perf_counter()
            model.simulate(timeModeling)
            end = time.perf_counter()
            execution_time_sum += end - start
            theoretical_sum += analyze_theoretical(model, timeModeling)
            
        theoretical_values.append(theoretical_sum / experiments_count)
        execution_time.append(execution_time_sum / experiments_count)

    
    plt.title("Аналітична оцінка")
    plt.xlabel("Складність моделі")
    plt.ylabel("Час виконання")
    plt.plot(events_count, execution_time, color="firebrick")
    plt.show()

    plt.title("Теоретична оцінка")
    plt.xlabel("Складність моделі")
    plt.ylabel("Операції")
    plt.plot(events_count, theoretical_values, color="firebrick")
    plt.show()

def analyze_different_events_count(create_model):

    # events_count = [40] #пусто
    # analyze(create_model, events_count)

    # events_count = [100, 200] #лінія
    # analyze(create_model, events_count)

    # events_count = [100, 200, 300, 400, 500]
    # analyze(create_model, events_count)

    events_count = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    analyze(create_model, events_count)