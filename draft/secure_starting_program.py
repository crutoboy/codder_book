import subprocess

def execute_python_proram(program: str, stdin: str) -> tuple:
    """
    Запуск python скрипта в докере

    Параметры:
    program: str - код программы
    stdin: str - входные данные

    Результат:
    Кортеж выходных данных и ошибок
    tupte(stdout, stderr)
    """

    cmd = [
        'docker', 'run', '--rm', '-i',
        '--cpus=0.5',
        '--memory=512m',
        '--network=none',
        '--read-only',
        'python:3.10-slim',
        'python', '-c', program
    ]
    proc = subprocess.run(cmd, input=stdin, text=True, timeout=5, capture_output=True)
    return (proc.stdout, proc.stderr)

def execute_cpp_proram(program: str, stdin: str) -> tuple:
    """
    Компиляция и запуск кода на c++

    Параметры:
    program: str - код программы
    stdin: str - входные данные

    Результат:
    Кортеж выходных данных и ошибок
    tupte(stdout, stderr)
    """

    cmd = [
        'docker', 'run', '--rm', '-i',
        '--cpus=0.5',
        '--memory=512m',
        '--network=none',
        'gcc:latest',
        'bash', '-c', f"echo '{program}' | g++ -x c++ - -o temp && ./temp"
    ]
    proc = subprocess.run(cmd, input=stdin, text=True, timeout=5, capture_output=True)
    return (proc.stdout, proc.stderr)

def start_program(program: str, stdin: str = '', language: str = 'python') -> str:
    """
    Безопасный запуск программ на различных языках программирования

    Параметры:
    program: str - код программы
    stdin: str - входные данные
    language: str - язык программирования, на котором написана прграмма
    Доступные значения: python, c++

    Результат:
    Кортеж выходных данных и ошибок
    tupte(stdout, stderr)
    """

    if language == 'python':
        return execute_python_proram(program, stdin)
    elif language == 'c++':
        return execute_cpp_proram(program, stdin)
    return (None, 'languge not support')


prog = """
n = int(input())
print('hello world', n)
"""

import pprint
# pprint.pprint(start_program(prog, '5', 'c++'))
pprint.pprint(start_program(prog, '5', 'python'))