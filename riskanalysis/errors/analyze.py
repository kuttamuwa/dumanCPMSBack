from appconfig.errors.base_exception import AppConfigBaseException


class BaseAnalyzeErrors(AppConfigBaseException):
    raise_state = True


class NoRiskDataset(BaseAnalyzeErrors):
    pass

