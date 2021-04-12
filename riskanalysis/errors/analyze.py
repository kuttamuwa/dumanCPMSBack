from appconfig.errors.base_exception import AppConfigBaseException


class BaseAnalyzeErrors(AppConfigBaseException):
    default_detail = "Analiz katmanında hata !"
    default_code = 500


class NoRiskDataset(BaseAnalyzeErrors):
    default_detail = "Risk dataset yok !"
    default_code = 400
