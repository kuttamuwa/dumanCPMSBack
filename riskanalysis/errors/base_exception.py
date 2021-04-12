"""

Tüm hatalar appconfig'teki hata sınıfından gelir, istersen burada ez
"""

from appconfig.errors.base_exception import AppConfigBaseException


class RiskAnalysisBaseException(AppConfigBaseException):
    default_detail = 'Risk analizi katmanında hata !'
    default_code = 500


