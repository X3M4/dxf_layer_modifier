import pandas as pd
import flet as ft
from models import csv_reader as rd

class CodeContainer(ft.Container):
    def __init__(self):
        super().__init__()
    
        self.dataframe = pd.DataFrame()
        
        # Campos de texto
        self.tfield_value = ft.TextField(
            label="Client Code",
            width="100%",
            text_size=24,
            max_length=6,
        )

        self.tfield_layer = ft.TextField(
            label="Layer Name",
            width="100%",
            text_size=24,
        )

        # Botón de agregar código
        self.add_button = ft.ElevatedButton(
            "Add Code",
            on_click=self.check_code,
            width="100%",
        )

        # Configurar contenido del contenedor
        self.content = ft.Column(
            
            [
                self.tfield_value,
                self.tfield_layer,
                self.add_button,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Configurar el contenedor principal
        self.margin = 10
        self.padding = 10
        self.alignment = ft.alignment.center
        self.bgcolor = ft.colors.AMBER
        self.width = 500
        self.height = 600
        self.border_radius = 10

    def check_code(self, e):
        """Obtiene los valores de los textfields y los guarda en el CSV"""
        value = self.tfield_value.value
        layer = self.tfield_layer.value
        
        csv_reader = rd.CSVReader()
        result = csv_reader.write_on_csv(value, layer)

        # Mostrar mensaje de confirmación
        self.content.controls.append(ft.Text(result, color="black" if "✅" in result else "red"))
        self.update()  # Refrescar la UI

