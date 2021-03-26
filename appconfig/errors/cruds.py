from appconfig.errors.base_exception import AppConfigBaseException


class CannotCreate(AppConfigBaseException):
    message = "Cannot be created !"
    raise_state = True
    item = None

    @classmethod
    def set_tr(cls):
        cls.message = f"{cls.item} oluşturulamadı !"

    @classmethod
    def set_en(cls):
        cls.message = f"{cls.item} cannot be created !"


class CannotUpdate(AppConfigBaseException):
    message = "Cannot be updated !"
    raise_state = True
    item = None

    @classmethod
    def set_tr(cls):
        cls.message = f"{cls.item} güncellenemedi !"

    @classmethod
    def set_en(cls):
        cls.message = f"{cls.item} cannot be updated !"


class CannotRead(AppConfigBaseException):
    message = "Cannot be read !"
    raise_state = False
    item = None

    @classmethod
    def set_tr(cls):
        cls.message = f"{cls.item} okunamadı !"

    @classmethod
    def set_en(cls):
        cls.message = f"{cls.item} cannot be read !"


class ImpossibleDecision(AppConfigBaseException):
    message = "Gerçekleştirilmesi mümkün olmayan bir işlem denendi !"
    raise_state = True

    item = None

    @classmethod
    def set_tr(cls):
        cls.message = "Gerçekleştirilmesi mümkün olmayan bir işlem denendi !"
        cls.message = f"{cls.item} üzerinde {cls.message}"

    @classmethod
    def set_en(cls):
        cls.message = "Unexpected demand failed ! "
        cls.message = f"{cls.message} on {cls.item}"
