from . import secure_execute_program
from .config import DEFAULT_CPU, DEFAULT_MEMORY, DEFAULT_TIMEOUT

def test_program(program: str, data_for_check: list[list[str]], language: str, \
    cpu=DEFAULT_CPU, memory=DEFAULT_MEMORY, timeout=DEFAULT_TIMEOUT):
    """
    тестирование передаваемых программ на соответствие вывода при определённом вводе

    Параметры:
    program: str - код программы
    data_for_check: list[list[str]] - двумерный список значений ввода и вывода
     [[stdin, stdout], [stdin, stdout], ...]
    language: str - язык программирования, на котором написана прграмма
     Доступные значения: см. secure_execute_program.start_program()
    cpu - параметр докера для ограничения процессорной мощности
    memory - параметр докера для ограничения ОЗУ
    timeout - параметр запуска программу для ограничения времени исполнения
    """



# start_program(program: str, stdin: str = '', language: str = 'python', \
#     cpu=DEFAULT_CPU, memory=DEFAULT_MEMORY, timeout=DEFAULT_TIMEOUT)