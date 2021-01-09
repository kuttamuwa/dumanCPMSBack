from appconfig.errors.base_exception import AppConfigBaseException


class CannotExceeds100(AppConfigBaseException):
    """
    Domain puanlarının toplamı 100'ü geçemez
    """

    message = "Cannot exceeds 100"
    item = None

    @classmethod
    def set_tr(cls):
        cls.message = "Puanların toplamı 100'ü geçemez !"

    @classmethod
    def set_en(cls):
        cls.message = "Sum of points cannot exceeds 100 !"

