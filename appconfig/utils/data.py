"""
Tüm modüller tarafından kullanılabilecek util kütüphanesi

"""


class DataValidation:
    @staticmethod
    def hate_none(*args):
        return all(*args)
