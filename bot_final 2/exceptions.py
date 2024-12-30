"""самописные ошибки"""
class BaseCustomException(Exception):
    """Базовое пользовательское исключение."""
    pass


class InvalidValueError(Exception):
    """Исключение для случаев некорректного значения."""
    def __init__(self, value, message="Некорректное значение"):
        self.value = value
        self.message = message
        super().__init__(f"{message}: {value}")


class CreateFileErr(Exception):
    def __init__(self, mgs, info):
        """Исклечение при ошибке создания файла"""
        super().__init__(mgs)
        self.info = info


class ReadErr(Exception):
    def __init__(self, mgs, info):
        """Исклечение при ошибке чтения файла"""
        super().__init__(mgs)
        self.info = info

