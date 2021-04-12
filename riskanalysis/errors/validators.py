from riskanalysis.errors.base_exception import RiskAnalysisBaseException


class BalanceError(RiskAnalysisBaseException):
    default_detail = "Bakiye verisi doldurulmalı, özellikle devir günü verilmediyse !"


class MaturitySpeedError(RiskAnalysisBaseException):
    default_detail = "Vade hızı verisi doldurulmamış"


class MaturityAvg12Balance(RiskAnalysisBaseException):
    default_detail = "Vade hızı boş verilmiş. Hızın bulunması için gerekli diğer veriler olan son "
    "12 aylık ortalama sipariş tutarı ve bakiye bilgileri de eksik. \n"
    "Algoritmanın sağlıklı çalışabilmesi için ilgili verileri lütfen doldurun !"


class AccountDoesNotExists(RiskAnalysisBaseException):
    default_detail = 'Hesap bulunamadı !'


class WarrantError(RiskAnalysisBaseException):
    default_detail = "Teminat bulunamadı !"


class WarrantAmountConflictError(RiskAnalysisBaseException):
    default_detail = "Teminat durumu yok denilmiş ama teminat tutarı girilmiş !"


class NoImplementedParameter(RiskAnalysisBaseException):
    default_detail = "Yanlış parametre verilmiş !"

