"""
Uygulamadaki tüm hatalar için base exception sınıfı
"""


class AppConfigBaseException(BaseException):
    raise_state = False
    message = None
    log = None

    """
    Tüm error sınıfları için base hata sınıfı. 
    :param raise_state:  True olursa hatalar raise olur, kaldırılır. False durumunda hata kaldırılmaz,
    loga düşer.
    
    :param message: Hata mesajı
    
    :param log: Loglama objesi
    """

    @classmethod
    def get_raise_state(cls):
        return cls.raise_state

    @classmethod
    def raise_on(cls):
        cls.raise_state = True

    @classmethod
    def raise_off(cls):
        cls.raise_state = False

    @classmethod
    def _log_info(cls, text):
        cls.log.info(text)

    @classmethod
    def _log_debug(cls, text):
        cls.log.debug(text)

    @classmethod
    def logging(cls, text, level):
        if level == 'info':
            cls._log_info(text)

        elif level == 'info':
            cls._log_debug(text)

    @classmethod
    def set_msg(cls, value):
        if value is not None:
            cls.message = value

    @classmethod
    def get_msg(cls):
        return cls.message

    @classmethod
    def set_tr(cls):
        pass

    @classmethod
    def set_en(cls):
        pass

    def raise_once(self):
        raise super(BaseException, self).__init__(self.message)

    def __init__(self, message=None, level='info'):
        self.set_msg(message)
        self.logging(message, level)

        if self.raise_state:
            raise super(AppConfigBaseException, self).__init__(self.message)
        else:
            pass


