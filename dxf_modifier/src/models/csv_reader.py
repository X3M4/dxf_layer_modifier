import pandas as pd

class CSVReader:
    def __init__(self, file_path="dxf_modifier/src/storage/data/Lista Capas.csv"):
        self.file_path = file_path
        self.dataframe = pd.DataFrame()

    def set_dataframe(self, csv):
        """Carga un CSV en un DataFrame asegurando que las columnas se leen correctamente."""
        try:
            self.file_path = csv
            # Leer CSV con el delimitador correcto
            df = pd.read_csv(csv, delimiter=",", encoding="latin-1", dtype=str)  # Convertir todo a string
            if "codigo_final" in df.columns and "codigo_inicial" in df.columns:
                self.dataframe = df
                print("✅ CSV cargado correctamente:")
                print(self.dataframe.head())  # Depuración
                return self.dataframe
            else:
                print("❌ Error: El CSV no tiene las columnas esperadas ('codigo_final', 'codigo_inicial').")
                return None
        except FileNotFoundError:
            print("❌ Error: No se encontró el archivo CSV.")
            return None
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return None

    def get_dataframe(self):
        """Devuelve el DataFrame de la instancia."""
        return self.dataframe

    def reload_dataframe(self):
        """Vuelve a leer el archivo CSV después de escribir en él."""
        try:
            print(f"♻️ Recargando DataFrame desde {self.file_path}...")
            self.dataframe = pd.read_csv(self.file_path, delimiter=",", encoding="latin-1", dtype=str)
            print("✅ DataFrame actualizado:")
            print(self.dataframe.head())
        except Exception as e:
            print(f"❌ Error al recargar DataFrame: {e}")

    def write_on_csv(self, value: str, layer: str):
        """Agrega un nuevo registro al CSV si el código y capa no existen en la misma fila."""
        try:
            df = self.dataframe
            if df.empty:
                print("❌ ERROR: El DataFrame está vacío después de cargar el CSV. ¿Seguro que el archivo tiene datos?")
                return "❌ No se puede escribir en el archivo porque no hay datos."

            # Validación de columnas
            if "codigo_final" not in df.columns or "codigo_inicial" not in df.columns:
                return "❌ Error: Las columnas esperadas no están en el CSV."

            # Limpiar valores
            value = value.strip().upper()
            layer = layer.strip().upper()

            # Normalizar valores en el DataFrame
            df["codigo_final"] = df["codigo_final"].astype(str).str.strip().str.upper()
            df["codigo_inicial"] = df["codigo_inicial"].astype(str).str.strip().str.upper()

            # Verificar si existe la combinación value-layer en la misma fila
            exists = ((df["codigo_final"] == value) & (df["codigo_inicial"] == layer)).any()
            if exists:
                return "⚠️ The combination of code and layer already exists."

            # Agregar nuevo registro
            new_register = pd.DataFrame([[value, layer]], columns=["codigo_final", "codigo_inicial"])
            new_register.to_csv(self.file_path, mode="a", header=False, index=False, sep=",", encoding="latin-1")

            # Recargar DataFrame después de escribir
            self.reload_dataframe()

            return f"✅ Client code and layer saved successfully: {value}, {layer}"

        except FileNotFoundError:
            return "❌ Error: CSV file was not found."
        except Exception as e:
            return f"❌ Error: {e}"

if __name__ == "__main__":
    csv_reader = CSVReader()
    
    # Prueba cargando un archivo
    df = csv_reader.set_dataframe("dxf_modifier/src/storage/data/Lista Capas.csv")
    if df is not None:
        print(df.head())

    # Prueba agregando un nuevo registro
    resultado = csv_reader.write_on_csv("168106", "ACCESO A PASO SUBTERRANEO")  # Código ya existe
    print(resultado)

    resultado = csv_reader.write_on_csv("059876", "NUEVA CAPA")  # Código nuevo
    print(resultado)
