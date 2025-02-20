import pandas as pd
import flet as ft
from models import csv_reader as rd
import ezdxf

class PosibleNewLayers(ft.Container):
    def __init__(self, page, csv_reader, modifier_container):
        super().__init__()
        
        self.page = page
        self.csv_reader = csv_reader
        self.modifier_container = modifier_container

        self.not_modified_layers = self.modifier_container.not_modified_layers  # Accedemos correctamente
        self.dataframe = self.csv_reader.get_dataframe()

        # Campos de texto
        self.file_name = ft.Text("Select the file to modify", width="100%")

        # Contenedor para nuevas filas
        self.new_layers_column = ft.Column(spacing=10)

        # Generar campos dinámicos según las capas no modificadas
        for layer in self.not_modified_layers:
            tfield_layer = ft.TextField(label="Layer Name", width="100%", text_size=24, value=layer, read_only=True)
            tfield_new_code = ft.TextField(label="New Layer Name", width="100%", text_size=24, max_length=6)

            button = ft.ElevatedButton("Add Layer", on_click=lambda e, l=tfield_layer, n=tfield_new_code: self.write_on_csv(e, l, n))

            self.new_layers_column.controls.append(ft.Row([tfield_layer, tfield_new_code, button]))

        # Agregar todo al contenedor principal
        self.content = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.file_name,
                            ft.Text("New Layers"),
                            self.new_layers_column
                        ],
                    ),
                    margin=ft.margin.only(left=230)
                )
            ]
        )

        self.page.update()

    def write_on_csv(self, e, tfield_layer, tfield_new_code):
        """Escribe en el CSV la nueva capa ingresada por el usuario."""
        if tfield_layer.value and tfield_new_code.value:
            self.csv_reader.write_on_csv(tfield_new_code.value, tfield_layer.value)
            self.page.snack_bar = ft.SnackBar(ft.Text("Layer added successfully"), open=True)
            self.page.update()
