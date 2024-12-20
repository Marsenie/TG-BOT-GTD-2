import numpy as np
from matplotlib import pyplot as plt

#тут мы создаем свой декоратор для валидациизначений о задачах, выполненных за посление две недели, для создания графика
class BaseCustomException(Exception):
    """Базовое пользовательское исключение."""
    pass

class InvalidValueError(BaseCustomException):
    """Исключение для случаев некорректного значения."""
    def __init__(self, value, message="Некорректное значение"):
        self.value = value
        self.message = message
        super().__init__(f"{message}: {value}")


def validate_value(condition, error_message="Некорректное значение"):
    """Декоратор для проверки значения аргументов."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for arg in args[1:]:
                if not condition(arg):
                    raise InvalidValueError(arg, error_message)
            return func(*args, **kwargs)
        return wrapper
    return decorator
  
#тут мы создаем график, на котором показанно сколько задач пользователь сделал за последние две недели
class Graph:
    def __init__(self, task_week_last, task_week_past):
        self.task_week_last = task_week_last
        self.task_week_past = task_week_past
        self.create_graph()

    @validate_value(lambda x: isinstance(x, int), "Аргумент должен быть целым числом")
    def create_graph(self):
        plt.figure(figsize=(8, 4))
        x = ['Last Week', 'This Week']
        y = [self.task_week_last, self.task_week_past]
        plt.bar(x, y)
        plt.title('График выполненных задач за последние две недели')
        plt.savefig('graphic.png', bbox_inches='tight') 
        plt.show()


