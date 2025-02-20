import pandas as pd
import flet as ft
from models import csv_reader as rd

class CodeContainer(ft.Container):
    def __init__(self, page, csv_reader):
        super().__init__()

        self.page = page
        self.dataframe = pd.DataFrame()
        self.csv_reader = csv_reader
        self.file_name = ft.Text("Select the file to modify", width="100%")
        
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
        
        self.file_picker = ft.FilePicker(
            on_result=self.pick_files_result
        )
        
        self.page.overlay.append(self.file_picker)

        # Botón de agregar código   
        self.add_button = ft.ElevatedButton(
            "Add Code",
            on_click=self.check_code,
            width="100%",
        )
        
        self.select_button = ft.ElevatedButton(
            "Pick CSV file",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files()
        )

        # Configurar contenido del contenedor
        self.content = ft.Column(
            
            [
                self.select_button,
                self.file_name,
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
        self.bgcolor = ft.colors.GREEN_500
        self.opacity = 0.8
        self.width = 350
        self.height = 300
        self.border_radius = 10
    
    def pick_files_result(self, e):
        """Obtiene el archivo seleccionado y lo guarda en el DataFrame."""
        if e.files:
            selected_file = e.files[0]
            print(f"📂 Archivo seleccionado: {selected_file.path}")  # Debug
            self.selected_file_path = selected_file.path  # Guardamos la ruta

            # Actualizar la UI con el nombre del archivo
            self.file_name.value = f"Selected file: {selected_file.name}"
            self.file_name.update()

            # Cargar el archivo en el DataFrame
            try:
                df = self.csv_reader.set_dataframe(self.selected_file_path)
                self.page.update()  # Actualizar la página
                if df is not None:
                    print("✅ DataFrame cargado correctamente:")
                    print(df.head())  # Ver los primeros datos
                else:
                    print("❌ El archivo CSV no se pudo cargar.")
            except Exception as ex:
                print(f"❌ Error al cargar CSV: {ex}")

            

    def check_code(self, e):
        """Obtiene los valores de los textfields y los guarda en el CSV"""
        value = self.tfield_value.value
        layer = self.tfield_layer.value
        
        result = self.csv_reader.write_on_csv(value, layer)

        # Mostrar mensaje de confirmación
        self.content.controls.append(ft.Text(result, color="black" if "✅" in result else "red"))
        self.update()  # Refrescar la UI

