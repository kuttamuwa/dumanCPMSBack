import pandas as pd
import os


class ImportExternalData:
    folder_path = r"C:\Users\LENOVO\PycharmProjects\dumanCPMSRevise\appconfig\data"
    vergiborcu = ""
    sgkborcu = ""
    sistemkaraliste = ""
    konkordataliste = ""

    def vergi_yukle(self):
        raise NotImplementedError

    def sgk_yukle(self):
        raise NotImplementedError

    def sistemkaraliste_yukle(self):
        raise NotImplementedError

    def konkordato_yukle(self):
        raise NotImplementedError

    def read_from_excel(self, filename):
        file_excel = os.path.join(self.folder_path, filename)
        df = pd.read_excel(file_excel)

        return df

    @staticmethod
    def _save(df):
        raise NotImplementedError

    def runforme(self):
        raise NotImplementedError
