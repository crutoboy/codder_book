import os
import subprocess
from uuid import uuid4

# default value
DEFAULT_CPU = 0.5
DEFAULT_MEMORY = '512m'
DEFAULT_TIMEOUT = 5
WORKSPACE = './workspace'


def execute_python_proram(program: str, stdin: str, \
    cpu=DEFAULT_CPU, memory=DEFAULT_MEMORY, timeout=DEFAULT_TIMEOUT) -> tuple[str, str]:
    """
    Запуск python скрипта в докере

    Параметры:
    program: str - код программы
    stdin: str - входные данные
    cpu - параметр докера для ограничения процессорной мощности
    memory - параметр докера для ограничения ОЗУ
    timeout - параметр запуска программу для ограничения времени исполнения

    Результат:
    Кортеж выходных данных и ошибок
    tupte(stdout, stderr)
    """

    cmd = [
        'docker', 'run', '--rm', '-i',
        f'--cpus={cpu}',
        f'--memory={memory}',
        '--network=none',
        '--read-only',
        'python:3.10-slim',
        'python', '-c', program
    ]
    proc = subprocess.run(cmd, input=stdin, text=True, timeout=timeout, capture_output=True)
    return (proc.stdout, proc.stderr)

def compile_cpp_program(program: str, compile_file: str, \
    cpu=DEFAULT_CPU, memory=DEFAULT_MEMORY, timeout=DEFAULT_TIMEOUT) -> tuple[str, str, str]:
    """
    Компиляция кода на c++ и возврат имени исполняемого файла

    Параметры:
    program: str - код программы
    cpu - параметр докера для ограничения процессорной мощности
    memory - параметр докера для ограничения ОЗУ
    timeout - параметр запуска программу для ограничения времени исполнения

    Результат:
    Кортеж выходных данных и ошибок
    tupte(id_program, stdout, stderr)
    """
    id_program = str(uuid4())
    path_to_program = os.path.join(WORKSPACE, id_program)
    os.makedirs(path_to_program)

    cmd = [
        'docker', 'run', '-i',
        f'--cpus={cpu}',
        f'--memory={memory}',
        '--network=none',
        '-v', f'{path_to_program}:/usr/src/app',
        'gcc:latest',
        "g++", "-x", "c++", "-", "-o", f'/usr/src/app/{compile_file}'
    ]
    proc = subprocess.run(cmd, input=program, text=True, timeout=timeout, capture_output=True)
    return (id_program, proc.stdout, proc.stderr)

def execute_cpp_proram(program: str, stdin: str, \
    cpu=DEFAULT_CPU, memory=DEFAULT_MEMORY, timeout=DEFAULT_TIMEOUT) -> tuple[str, str, str]:
    """
    Компиляция и запуск кода на c++

    Параметры:
    program: str - код программы
    stdin: str - входные данные
    cpu - параметр докера для ограничения процессорной мощности
    memory - параметр докера для ограничения ОЗУ
    timeout - параметр запуска программу для ограничения времени исполнения

    Результат:
    Кортеж выходных данных и ошибок
    tupte(id_program, stdout, stderr)
    """
    compile_file = 'cpp_program'
    id_program, compile_stdout, compile_stderr = compile_cpp_program(program, compile_file, cpu, memory, timeout)
    path_to_program = os.path.join(WORKSPACE, id_program)

    if compile_stderr != '':
        return ('', 'compile error:\n' + compile_stderr)
    if not os.path.isfile(os.path.join(path_to_program, compile_file)):
        return ('', 'compile error:\ncompiling file not exists')

    cmd = [
        'docker', 'run', '--rm', '-i',
        f'--cpus={cpu}',
        f'--memory={memory}',
        '--network=none',
        '--read-only',
        '-v', f'{path_to_program}:/usr/src/app',
        'gcc:latest', f'/usr/src/app/{compile_file}'
    ]
    proc = subprocess.run(cmd, input=stdin, text=True, timeout=timeout, capture_output=True)
    return (id_program, proc.stdout, proc.stderr)

def start_program(program: str, stdin: str = '', language: str = 'python', \
    cpu=DEFAULT_CPU, memory=DEFAULT_MEMORY, timeout=DEFAULT_TIMEOUT) -> tuple[str, str]:
    """
    Безопасный запуск программ на различных языках программирования

    Параметры:
    program: str - код программы
    stdin: str - входные данные
    language: str - язык программирования, на котором написана прграмма
     Доступные значения: python, cpp
    cpu - параметр докера для ограничения процессорной мощности
    memory - параметр докера для ограничения ОЗУ
    timeout - параметр запуска программу для ограничения времени исполнения

    Результат:
    Кортеж выходных данных и ошибок
    tupte(stdout, stderr)
    """

    if language == 'python':
        return execute_python_proram(program, stdin, cpu, memory, timeout)
    elif language == 'cpp':
        _, stdout, stderr = execute_cpp_proram(program, stdin, cpu, memory, timeout)
        return (stdout, stderr)
    return ('', 'languge not support')


