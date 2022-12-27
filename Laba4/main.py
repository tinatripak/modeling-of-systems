import createAndTest
import Analyzer.analyzer as analyzer

print('Розробити модель масового обслуговування, яка складається з N систем масового обслуговування\n' +
      'Виконати експериментальну і теоретичну оцінку складності алгоритму імітації мережі масового обслуговування')

analyzer.analyze_different_events_count(createAndTest.create_mass_service_model)
# analyzer.analyze_different_events_count(createAndTest.create_system)