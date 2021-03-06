"""

Tüm hatalar appconfig'teki hata sınıfından gelir, istersen burada ez
"""

from appconfig.errors.base_exception import AppConfigBaseException


class RiskAnalysisBaseException(AppConfigBaseException):
    pass


