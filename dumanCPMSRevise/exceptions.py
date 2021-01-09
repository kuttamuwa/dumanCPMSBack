from abc import ABC

from dumanCPMSRevise import settings


class DumanMessageInterface(ABC):
    lang = settings.LANGUAGE_CODE

    @classmethod
    def switch_tr(cls, value):
        settings.LANGUAGE_CODE = 'tr-tr'

    @classmethod
    def translate_message(cls):
        pass

    @classmethod
    def translate_errors(cls):
        pass