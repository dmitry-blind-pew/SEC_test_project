class SecTestException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ApiKeyInvalidException(SecTestException):
    detail = "API ключ неверный или отсутствует"


class ObjectNotFoundException(SecTestException):
    detail = "Объект не найден"


class CompanyNotFoundException(ObjectNotFoundException):
    detail = "Компания не найдена"


class InvalidRectangleBoundsException(SecTestException):
    detail = "Некорректные границы области: min должен быть <= max"
