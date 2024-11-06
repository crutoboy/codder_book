import os
import subprocess
from uuid import uuid4

from .config import DEFAULT_CPU, DEFAULT_MEMORY, DEFAULT_TIMEOUT, WORKSPACE


def execute_python_proram(program: str, stdin: str, \
    cpu:float=DEFAULT_CPU, memory:float=DEFAULT_MEMORY, timeout:float=DEFAULT_TIMEOUT) -> tuple[str, str]:
    """
    Выполняет Python скрипт в изолированном Docker-контейнере с ограничениями.

    Параметры:
    - program (str): Код программы на Python.
    - stdin (str): Входные данные, подаваемые программе.
    - cpu (float): Ограничение на использование процессора в контейнере.
    - memory (float): Ограничение на использование памяти в контейнере.
    - timeout (float): Лимит времени выполнения программы в секундах.

    Результат:
    tuple[str, str]: Кортеж (stdout, stderr) с результатом выполнения и сообщениями об ошибках.
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
    try:
        proc = subprocess.run(cmd, input=stdin, text=True, timeout=timeout, capture_output=True)
    except subprocess.TimeoutExpired:
        return ('', f'executing error:\ntimeout error ({timeout}s)')
    return (proc.stdout, proc.stderr)

def compile_cpp_program(program: str, compile_file: str, \
    cpu:float=DEFAULT_CPU, memory:float=DEFAULT_MEMORY, timeout:float=DEFAULT_TIMEOUT) -> tuple[str, str, str]:
    """
    Компилирует C++ программу и возвращает ID программы и информацию об ошибках.

    Параметры:
    - program (str): Код программы на C++.
    - compile_file (str): Имя для скомпилированного файла.
    - cpu (float): Ограничение на использование процессора.
    - memory (float): Ограничение на использование памяти.
    - timeout (float): Лимит времени компиляции.

    Результат:
    tuple[str, str, str]: Кортеж (id_program, stdout, stderr), где id_program — ID папки с программой,
                          stdout — стандартный вывод, stderr — сообщения об ошибках.
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
    try:
        proc = subprocess.run(cmd, input=program, text=True, timeout=timeout, capture_output=True)
    except subprocess.TimeoutExpired:
        return (id_program, '', f'compile error:\ntimeout error ({timeout}s)')
    return (id_program, proc.stdout, proc.stderr)

def execute_cpp_proram(program: str, stdin: str, \
    cpu:float=DEFAULT_CPU, memory:float=DEFAULT_MEMORY, timeout:float=DEFAULT_TIMEOUT) -> tuple[str, str, str]:
    """
    Компилирует и выполняет программу на C++ в изолированном контейнере.

    Параметры:
    - program (str): Код программы на C++.
    - stdin (str): Входные данные для программы.
    - cpu (float): Ограничение на использование процессора.
    - memory (float): Ограничение на использование памяти.
    - timeout (float): Лимит времени выполнения.

    Результат:
    tuple[str, str, str]: Кортеж (id_program, stdout, stderr), где id_program — ID папки с программой,
                          stdout — стандартный вывод, stderr — сообщения об ошибках.
    """
    compile_file = 'cpp_program'
    id_program, compile_stdout, compile_stderr = compile_cpp_program(program, compile_file, cpu, memory, timeout)
    path_to_program = os.path.join(WORKSPACE, id_program)

    if compile_stderr != '':
        return (id_program,'', 'compile error:\n' + compile_stderr)
    if not os.path.isfile(os.path.join(path_to_program, compile_file)):
        return (id_program, '', 'compile error:\ncompiling file not exists')

    cmd = [
        'docker', 'run', '--rm', '-i',
        f'--cpus={cpu}',
        f'--memory={memory}',
        '--network=none',
        '--read-only',
        '-v', f'{path_to_program}:/usr/src/app',
        'gcc:latest', f'/usr/src/app/{compile_file}'
    ]
    try:
        proc = subprocess.run(cmd, input=stdin, text=True, timeout=timeout, capture_output=True)
    except subprocess.TimeoutExpired:
        return (id_program, '', f'executing error:\ntimeout error ({timeout}s)')
    return (id_program, proc.stdout, proc.stderr)

def start_program(program: str, stdin: str = '', language: str = 'python', \
    cpu:float=DEFAULT_CPU, memory:float=DEFAULT_MEMORY, timeout:float=DEFAULT_TIMEOUT) -> tuple[str, str]:
    """
    Выполняет программы на различных языках программирования в изолированном окружении.

    Параметры:
    - program (str): Код программы.
    - stdin (str): Входные данные.
    - language (str): Язык программирования (поддерживается: 'python', 'cpp').
    - cpu (float): Ограничение на использование процессора.
    - memory (float): Ограничение на использование памяти.
    - timeout (float): Лимит времени выполнения.

    Результат:
    tuple[str, str]: Кортеж (stdout, stderr) с результатами выполнения и сообщениями об ошибках.
    """

    if language == 'python':
        return execute_python_proram(program, stdin, cpu, memory, timeout)
    elif language == 'cpp':
        _, stdout, stderr = execute_cpp_proram(program, stdin, cpu, memory, timeout)
        return (stdout, stderr)
    return ('', 'languge not support')


