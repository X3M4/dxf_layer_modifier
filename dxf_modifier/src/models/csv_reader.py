import pandas as pd

class CSVReader:
    file_path = ""
    dataframe = pd.DataFrame()
    
    def __init__(self):
        self.file_path = "dxf_modifier/src/storage/data/Lista Capas.csv"

    def read_csv(self):
        self.dataframe = pd.read_csv(self.file_path, delimiter=";", encoding="latin-1")
        self.dataframe = self.dataframe.dropna(axis=1, how="all")
        
        if self.dataframe is not None:
            return self.dataframe
        else:
            return "El archivo no se ha podido leer"

if __name__ == "__main__":
    csv_reader = CSVReader()
    df = csv_reader.read_csv()
    if df is not None:
        print(df.head())
        print(df.count)
    else:
        print("Imposible leer archivo")
            