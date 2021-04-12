from appconfig.errors.base_exception import AppConfigBaseException


class CannotCreate(AppConfigBaseException):
    default_detail = 'Obje oluşturulamadı !'


class CannotUpdate(AppConfigBaseException):
    default_detail = "Obje güncellenemedi !"


class CannotRead(AppConfigBaseException):
    default_detail = "Obje okunamadı !"


class ImpossibleDecision(AppConfigBaseException):
    default_detail = "Gerçekleştirilmesi mümkün olmayan bir işlem denendi !"
