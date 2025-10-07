# def fence(func):
#     def wrapper():
#         print("+" * 10)
#         func()
#         print("+" * 10)

#     return wrapper


# @fence
# def log():
#     print("decorated!")

from typing import Callable, Any


def custom_fence(fence: str = "+"):
    def add_fence(func):
        def wrapper(text: str):
            print(fence * len(text))
            func(text)
            print(fence * len(text))

        return wrapper

    return add_fence


@custom_fence("-")
def log(text: str):
    print(text)


def decorator(func: Callable[[Any], None]):
    pass


log("syp")
