from riskanalysis.errors.base_exception import RiskAnalysisBaseException


class RiskDatasetCannotCreate(RiskAnalysisBaseException):
    message = "Cannot be created !"
    raise_state = True
    item = None

    @classmethod
    def set_tr(cls):
        cls.message = f"{cls.item} oluşturulamadı !"

    @classmethod
    def set_en(cls):
        cls.message = f"{cls.item} cannot be created !"


class RiskDatasetCannotUpdate(RiskAnalysisBaseException):
    message = "Cannot be updated !"
    raise_state = True
    item = None

    @classmethod
    def set_tr(cls):
        cls.message = f"{cls.item} güncellenemedi !"

    @classmethod
    def set_en(cls):
        cls.message = f"{cls.item} cannot be updated !"


class RiskDatasetCannotRead(RiskAnalysisBaseException):
    message = "Cannot be read !"
    raise_state = False
    item = None

    @classmethod
    def set_tr(cls):
        cls.message = f"{cls.item} okunamadı !"

    @classmethod
    def set_en(cls):
        cls.message = f"{cls.item} cannot be read !"