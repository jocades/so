from typing import Callable


class P:
    def __init__(self, name):
        self.name: str = name
        self.age: int
        self.say_hello: Callable


def get_person(name: str):
    return P(name)


def use_person(name, func):
    return func(get_person(name))


def manager(person: P):
    person.age = 10
    return person


person = use_person('Jordi', manager)

person.say_hello = lambda: print(f"Hello {person.name}")
person.say_hello()

print(person.__dict__)
