import subprocess

from .. import workspace_tool
from ..config import DEFAULT_CPU, DEFAULT_MEMORY, DEFAULT_TIMEOUT


COMPILING_FILE_NAME = 'compile_cpp_program'


def compile_cpp_program(program: str, workspace_id: str, \
    cpu:float=DEFAULT_CPU, memory:int=DEFAULT_MEMORY, timeout:float=DEFAULT_TIMEOUT) -> tuple[str, str, str]:
    """
    Компилирует C++ программу и возвращает ID программы и информацию об ошибках.

    Параметры:
    - program (str): Код программы на C++.
    - compile_file (str): Имя для скомпилированного файла.
    - cpu (float): Ограничение на использование процессора.
    - memory (int): Ограничение на использование памяти в мегабайтах.
    - timeout (float): Лимит времени компиляции.

    Результат:
    tuple[str, str, str]: Кортеж (id_program, stdout, stderr), где id_program — ID папки с программой,
                          stdout — стандартный вывод, stderr — сообщения об ошибках.
    """

    path_to_workspace = workspace_tool.get_path_to_workspace(workspace_id)

    cmd = [
        'docker', 'run', '-i',
        f'--cpus={cpu}',
        f'--memory={memory}m',
        '--network=none',
        '-v', f'{path_to_workspace}:/usr/src/app',
        'gcc:latest',
        "g++", "-x", "c++", "-", "-o", f'/usr/src/app/{COMPILING_FILE_NAME}'
    ]
    try:
        proc = subprocess.run(cmd, input=program, text=True, timeout=timeout, capture_output=True)
    except subprocess.TimeoutExpired:
        return ('', f'compile error:\ntimeout error ({timeout}s)', 'ce')
    return (proc.stdout, proc.stderr, proc.returncode)


def run_cpp_program(workspace_id: str, stdin: str, \
    cpu:float=DEFAULT_CPU, memory:int=DEFAULT_MEMORY, timeout:float=DEFAULT_TIMEOUT) -> tuple[str, str, str]:
    """запуск c++ программы"""

    path_to_workspace = workspace_tool.get_path_to_workspace(workspace_id)

    cmd = [
        'docker', 'run', '--rm', '-i',
        f'--cpus={cpu}',
        f'--memory={memory}m',
        '--network=none',
        '--read-only',
        '-v', f'{path_to_workspace}:/usr/src/app',
        'gcc:latest', f'/usr/src/app/{COMPILING_FILE_NAME}'
    ]
    try:
        proc = subprocess.run(cmd, input=stdin, text=True, timeout=timeout, capture_output=True)
    except subprocess.TimeoutExpired:
        return ('', f'runtime error:\ntimeout error ({timeout}s)', 're')
    return (proc.stdout, proc.stderr, proc.returncode)


def execute_cpp_proram(program: str, stdin: str, \
    cpu:float=DEFAULT_CPU, memory:int=DEFAULT_MEMORY, timeout:float=DEFAULT_TIMEOUT) -> tuple[str, str, str]:

    id_workspace = workspace_tool.create_workspace() # создания пространства для сохранения временных файлов для исполнения программы

    compile_stdout, compile_stderr, compile_returncode = compile_cpp_program(program, id_workspace, cpu, memory, timeout)
    if compile_returncode != 0:
        workspace_tool.del_workspace(id_workspace) # удаление временного пространства с промежуточными файлами
        return (compile_stdout, compile_stderr, 'ce')

    exec_stdout, exec_stderr, exec_returncode = run_cpp_program(id_workspace, stdin, cpu, memory, timeout)

    workspace_tool.del_workspace(id_workspace) # удаление временного пространства с промежуточными файлами

    if exec_returncode != 0:
        return (exec_stdout, exec_stderr, 're')
    return (exec_stdout, exec_stderr, 'ne')