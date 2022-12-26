from taskModel import TaskModel

tasks = TaskModel()

print('Реалізація універсального алгоритму імітації моделі масового обслуговування з багатоканальним обслуговуванням')
tasks.get_model_with_multichannel_service()

print('Реалізація універсального алгоритму імітації моделі масового обслуговування з вибором маршруту за пріоритетом')
tasks.get_model_with_priority_route_selection()

print('Реалізація універсального алгоритму імітації моделі масового обслуговування з вибором маршруту за заданою ймовірністю')
tasks.get_model_with_given_probability()

print('Реалізація банкової моделі')
tasks.get_bank_model()

print('Реалізація лікарняної моделі')
tasks.get_hospital_model()