from rich import print
from pathlib import Path
from enum import Enum


def fn(arg1: str, arg2: int):
    print(arg1)
    print(arg2)


print('sizeof', fn.__sizeof__())
print('code', fn.__code__)
print('code.argcount', fn.__code__.co_argcount)

# how to get the parameters names?
print('code.co_varnames', fn.__code__.co_varnames)

# how to get the parameters annotations?
print('annotations', fn.__annotations__)

print(f"[blue]Start fresh[/] new project? {'[y/N]'}")
# res = input('> ').lower()

# if res in 'nN':
#     print('bye')
#     exit()
# elif res in 'yY':
#     print('ok')
# else:
#     raise Exception('Invalid input')


def no(x: str, n):
    print(x, n)
    locals()['n'] = 2
    print(x, n)


no('a', 1)
