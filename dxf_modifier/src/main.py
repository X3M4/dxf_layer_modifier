import flet as ft
import pandas as pd
from models import csv_reader as rd  # Asegúrate de que el import es correcto

class DataFrameViewer(ft.Column):
    def __init__(self):
        super().__init__()
        self.dataframe = pd.DataFrame()

        # Inicializa la tabla con una columna vacía para evitar el error
        self.datatable = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(""))],  # Columna temporal
            rows=[]
        )

        self.load_button = ft.ElevatedButton("Cargar CSV", on_click=self.load_data)

        # Agregamos el botón y la tabla vacía al inicio
        self.controls = [
            ft.Text("Visor de CSV", size=24, weight=ft.FontWeight.BOLD),
            self.load_button,
            self.datatable,
        ]

    def load_data(self, e):
        """Carga el CSV y actualiza la tabla"""
        csv_reader = rd.CSVReader()
        self.dataframe = csv_reader.read_csv()

        if self.dataframe is None or self.dataframe.empty:
            self.controls.append(ft.Text("Error al cargar el CSV o archivo vacío.", color="red"))
            self.update()
            return

        # Configurar columnas del DataTable con los nombres del DataFrame
        self.datatable.columns = [ft.DataColumn(ft.Text(col)) for col in self.dataframe.columns]

        # Agregar filas con datos
        self.datatable.rows = [
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(value))) for value in row]
            )
            for row in self.dataframe.values
        ]

        self.update()  # Refrescar la UI

def main(page: ft.Page):
    page.title = "DXF Modifier"
    page.scroll = "adaptive"
    
    # Agregar la vista del DataFrame con botón
    page.add(DataFrameViewer())

ft.app(target=main)
