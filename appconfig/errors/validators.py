from appconfig.errors.base_exception import AppConfigBaseException


class CannotExceeds100(AppConfigBaseException):
    """
    Domain puanlarının toplamı 100'ü geçemez
    """

    default_detail = "Toplamları 100'ü geçemez !"
