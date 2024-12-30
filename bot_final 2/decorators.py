"""декораторы"""
from exceptions import *


#создаем свой декоратор для валидациизначений о задачах, выполненных за посление две недели, для создания графика
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
