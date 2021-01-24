from riskanalysis.errors.base_exception import RiskAnalysisBaseException


class BalanceError(RiskAnalysisBaseException):
    message = "Bakiye verisi doldurulmalı, özellikle devir günü verilmediyse !"


class MaturitySpeedError(RiskAnalysisBaseException):
    message = "Vade hızı verisi doldurulmamış"


class MaturityAvg12Balance(RiskAnalysisBaseException):
    message = "Vade hızı boş verilmiş. Hızın bulunması için gerekli diğer veriler olan son "
    "12 aylık ortalama sipariş tutarı ve bakiye bilgileri de eksik. \n"
    "Algoritmanın sağlıklı çalışabilmesi için ilgili verileri lütfen doldurun !"


class AccountDoesNotExists(RiskAnalysisBaseException):
    message = 'Hesap bulunamadı !'


class WarrantError(RiskAnalysisBaseException):
    message = "Teminat bulunamadı !"


class WarrantAmountConflictError(RiskAnalysisBaseException):
    message = "Teminat durumu yok denilmiş ama teminat tutarı girilmiş !"


class NoImplementedParameter(RiskAnalysisBaseException):
    message = "Yanlış parametre verilmiş !"

