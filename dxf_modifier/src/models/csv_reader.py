import pandas as pd

class CSVReader:
    def __init__(self):
        self.file_path = "dxf_modifier/src/storage/data/Lista Capas.csv"
        self.dataframe = pd.DataFrame()

    def read_csv(self):
        """Lee el archivo CSV y actualiza el DataFrame."""
        try:
            self.dataframe = pd.read_csv(self.file_path, delimiter=";", encoding="latin-1")
            self.dataframe = self.dataframe.dropna(axis=1, how="all")  # Elimina columnas vacías
            return self.dataframe
        except FileNotFoundError:
            print("❌ Error: No se encontró el archivo CSV.")
            return None
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return None

    def write_on_csv(self, value: str, layer: str):
        """Agrega un nuevo registro al CSV si el código y layer no existen en la misma fila."""
        try:
            df = self.read_csv()
            if df is None:
                return "❌ No se puede escribir en el archivo porque no existe."

            if df.shape[1] < 2:
                return "❌ Error: El archivo CSV no tiene suficientes columnas."

            # Limpiar valores
            value = value.strip().upper()
            layer = layer.strip().upper()

            # Obtener nombres de columnas
            code_column = df.columns[0]  # Primera columna
            layer_column = df.columns[1]  # Segunda columna

            # Normalizar valores en el DataFrame
            df[code_column] = df[code_column].astype(str).str.strip().str.upper()
            df[layer_column] = df[layer_column].astype(str).str.strip().str.upper()

            # Verificar si existe la combinación value-layer en la misma fila
            exists = ((df[code_column] == value) & (df[layer_column] == layer)).any()
            
            if exists:
                return "⚠️ The combination of code and layer already exists."

            # Agregar nuevo registro
            new_register = pd.DataFrame([[value, layer]], columns=df.columns[:2])
            new_register.to_csv(self.file_path, mode="a", header=False, index=False, sep=";", encoding="latin-1")

            # Recargar DataFrame
            self.read_csv()
            return f"✅ Client code and layer saved successfully: {value}, {layer}"

        except FileNotFoundError:
            return "❌ Error: CSV file was not found."
        except Exception as e:
            return f"❌ Error: {e}"

if __name__ == "__main__":
    csv_reader = CSVReader()
    
    # Prueba agregando un nuevo registro
    resultado = csv_reader.write_on_csv("168106", "COSA")  # Código ya existe
    print(resultado)

    cola = csv_reader.read_csv()
    resultado = csv_reader.write_on_csv("059876", "COSA")  # Código nuevo
    print(resultado)
    print(cola)
