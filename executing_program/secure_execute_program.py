import os
import subprocess
from uuid import uuid4

from . import programing_languages
from .config import DEFAULT_CPU, DEFAULT_MEMORY, DEFAULT_TIMEOUT, WORKSPACE


def start_program(program: str, stdin: str = '', language: str = 'python', \
    cpu:float=DEFAULT_CPU, memory:int=DEFAULT_MEMORY, timeout:float=DEFAULT_TIMEOUT) -> tuple[str, str, str]:
    """
    Выполняет программы на различных языках программирования в изолированном окружении.

    Параметры:
    - program (str): Код программы.
    - stdin (str): Входные данные.
    - language (str): Язык программирования (поддерживается: 'python', 'cpp').
    - cpu (float): Ограничение на использование процессора.
    - memory (int): Ограничение на использование памяти в мегабайтах.
    - timeout (float): Лимит времени выполнения.

    Результат:
    tuple[str, str, str]: Кортеж (stdout, stderr, status_code) с результатами выполнения, сообщениями об ошибках и кодом о статусе выполнения.
    """

    if language == 'python':
        stdout, stderr, status_code = programing_languages.python_exec.execute_python_proram(program, stdin, cpu, memory, timeout)
        return (stdout, stderr, status_code)
    elif language == 'cpp':
        stdout, stderr, status_code = programing_languages.cpp_exec.execute_cpp_proram(program, stdin, cpu, memory, timeout)
        return (stdout, stderr, status_code)
    return ('', 'languge not support', None)

