import pandas as pd

from create import Create
from model import Model
from process import Process


class SimModel():
    def task_first(self):
        creator = Create(5)
        firstProcess = Process(5)
        firstProcess.maxqueue = 5

        creator.distribution = 'exp'
        firstProcess.distribution = 'exp'
        creator.name = 'Створювач опрацьованих елементів процесом Create'
        firstProcess.name = 'Процес перший'

        creator.nextElement = [firstProcess]
        elements = [creator, firstProcess]
        model = Model(elements)
        model.simulate(1000)

    def task_third(self):
        creator = Create(5)
        firstProcess = Process(5)
        secondProcess = Process(5)
        thirdProcess = Process(5)

        creator.nextElement = [firstProcess]
        firstProcess.nextElement = [secondProcess]
        secondProcess.nextElement = [thirdProcess]
        
        firstProcess.maxqueue = 5
        secondProcess.maxqueue = 5
        thirdProcess.maxqueue = 5
        
        creator.distribution = 'exp'
        firstProcess.distribution = 'exp'
        secondProcess.distribution = 'exp'
        thirdProcess.distribution = 'exp'

        creator.name = 'Створювач'
        firstProcess.name = 'Процес перший'
        secondProcess.name = 'Процес другий'
        thirdProcess.name = 'Процес третій'
        
        mass = [creator, firstProcess, secondProcess, thirdProcess]
        model = Model(mass)
        model.simulate(1000)

    def task_fourth(self):
        creator_array = [4, 10, 4, 4, 4, 4, 4, 4, 0.5, 4, 4, 4, 4, 4, 4]
        
        process_array = [
            [4, 4, 10, 4, 4, 4, 4, 4, 4, 0.5, 4, 4, 4, 4, 4],
            [4, 4, 4, 10, 4, 4, 4, 4, 4, 4, 0.5, 4, 4, 4, 4],
            [4, 4, 4, 4, 10, 4, 4, 4, 4, 4, 4, 0.5, 4, 4, 4]
        ]

        maxqueue_array = [
            [5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 5, 5],
            [5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 5],
            [5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1],
        ]

        results = []

        for i in range(len(creator_array)):
            creator = Create(creator_array[i])

            firstProcess = Process(process_array[0][i])
            secondProcess = Process(process_array[1][i])
            thirdProcess = Process(process_array[2][i])

            firstProcess.maxqueue = maxqueue_array[0][i]
            secondProcess.maxqueue = maxqueue_array[1][i]
            thirdProcess.maxqueue = maxqueue_array[2][i]

            creator.distribution = 'exp'
            firstProcess.distribution = 'exp'
            secondProcess.distribution = 'exp'
            thirdProcess.distribution = 'exp'

            creator.name = 'Створювач'
            firstProcess.name = 'Процес перший'
            secondProcess.name = 'Процес другий'
            thirdProcess.name = 'Процес третій'

            creator.nextElement = [firstProcess]
            firstProcess.nextElement = [secondProcess]
            secondProcess.nextElement = [thirdProcess]

            mass = [creator, firstProcess, secondProcess, thirdProcess]
            model = Model(mass)
            model.simulate(1000)

            results.append([creator_array[i],
                process_array[0][i],
                process_array[1][i],
                process_array[2][i],
                maxqueue_array[0][i],
                maxqueue_array[1][i],
                maxqueue_array[2][i],
                firstProcess.quantity,
                firstProcess.failure,
                secondProcess.quantity,
                secondProcess.failure,
                thirdProcess.quantity,
                thirdProcess.failure])

        columns = [
            'Створювач часової затримки',
            'Перший процес часової затримки',
            'Другий процес часової затримки',
            'Третій процес часової затримки',
            'Перша максимальна черга',
            'Друга максимальна черга',
            'Третя максимальна черга',
            'Перший процес - успіх',
            'Перший процес - невдача',
            'Другий процес - успіх',
            'Другий процес - невдача',
            'Третій процес - успіх',
            'Третій процес - невдача'
        ]

        df = pd.DataFrame(results, columns=columns)
        print(f"Розподіл: {distribution}")
        print(df)
        

    def task_fifth(self):
        creator = Create(5)
        firstProcess = Process(5, 2)
        firstProcess.maxqueue = 5

        creator.distribution = 'exp'
        firstProcess.distribution = 'exp'
        creator.name = 'Створювач'
        firstProcess.name = 'Процес перший'

        creator.nextElement = [firstProcess]
        elements = [creator, firstProcess]
        model = Model(elements)
        model.simulate(1000)


    def task_sixth(self):
        creator = Create(5)
        firstProcess = Process(5)
        secondProcess = Process(5)
        thirdProcess = Process(5)

        creator.nextElement = [firstProcess]
        firstProcess.nextElement = [secondProcess, thirdProcess]

        firstProcess.probability = ([0.7, 0.3])

        firstProcess.maxqueue = 5
        secondProcess.maxqueue = 5
        thirdProcess.maxqueue = 5

        creator.distribution = 'exp'
        firstProcess.distribution = 'exp'
        secondProcess.distribution = 'exp'
        thirdProcess.distribution = 'exp'

        creator.name = 'Створювач'
        firstProcess.name = 'Процес перший'
        secondProcess.name = 'Процес другий'
        thirdProcess.name = 'Процес третій'

        elements = [creator, firstProcess, secondProcess, thirdProcess]
        model = Model(elements)
        model.simulate(1000)
