import contextlib
import os
import subprocess


@contextlib.contextmanager
def chdir(wd):
    cwd = os.getcwd()
    os.chdir(wd)
    try:
        yield wd
    finally:
        os.chdir(cwd)


def call(text):
    print(f'$ {text}')
    return subprocess.call(text, shell=True)


def recv_int_from_stdin(name, default):
    s = input(f"{name}({default}): ")
    if s:
        return int(s)
    return default


def recv_str_from_stdin(name, default):
    s = input(f"{name}({default}): ")
    if s:
        return s
    return default
