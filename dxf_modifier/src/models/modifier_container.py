import pandas as pd
import flet as ft
from models import csv_reader as rd
import ezdxf

class ModifierContainer(ft.Container):
    def __init__(self, page, csv_reader):
        super().__init__()
        
        self.page = page
        
        self.csv_reader = csv_reader
        
        self.dataframe = self.csv_reader.get_dataframe()
        
        # Campos de texto
        self.file_name = ft.Text("Select the file to modify", width="100%")

        # Initialize FilePicker with correct parameters
        self.file_picker = ft.FilePicker(
            on_result=self.pick_files_result
        )
        
        self.page.overlay.append(self.file_picker)

        # Botón de selección
        self.select_button = ft.ElevatedButton(
            "Pick DXF file",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files()
        )
        
        self.modify_button = ft.ElevatedButton(
            "Modify DXF",
            icon=ft.icons.VERIFIED,
            on_click=self.modify_dxf
        )

        # Configure content
        self.content = ft.Column(
            [
                self.file_name,
                self.select_button,
                self.modify_button,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Configure container
        self.margin = 10
        self.padding = 10
        self.alignment = ft.alignment.center
        self.bgcolor = ft.colors.AMBER
        self.width = 350
        self.height = 350
        self.border_radius = 10

    def pick_files_result(self, e):
        """Guarda la ruta del archivo DXF sin tocar el DataFrame."""
        if e.files:
            selected_file = e.files[0]
            print(f"📂 Archivo DXF seleccionado: {selected_file.path}")  # Debug

            self.file_name.value = f"Selected file: {selected_file.name}"
            self.file_name.update()

            # 🔹 Guardar la ruta del DXF para modificarlo después
            self.dxf_file_path = selected_file.path  

            print("✅ Archivo DXF listo para modificar.")


    
    def modify_dxf(self, e):
        print("modify_dxf fue llamado")  

        if not self.file_picker.result or not self.file_picker.result.files:
            print("❌ No hay archivo DXF seleccionado.")  
            self.page.snack_bar = ft.SnackBar(ft.Text("No DXF file selected"), open=True)
            self.page.update()
            return

        file_path = self.file_picker.result.files[0].path
        print(f"📂 Procesando archivo DXF: {file_path}")

        # 🔹 Obtener los datos actualizados antes de modificar
        self.dataframe = self.csv_reader.get_dataframe()

        print("📊 Estado actual del DataFrame antes de modificar DXF:")
        print(self.dataframe)

        if self.dataframe is None or self.dataframe.empty:
            print("❌ Error: El DataFrame está vacío antes de modificar el DXF.")
            self.page.snack_bar = ft.SnackBar(ft.Text("No data loaded from CSV"), open=True)
            self.page.update()
            return

        try:
            # Verificar que el DataFrame tiene al menos dos columnas
            if self.dataframe is None or self.dataframe.empty:
                print("❌ Error: El DataFrame está vacío.")
                self.page.snack_bar = ft.SnackBar(ft.Text("No data loaded from CSV"), open=True)
                self.page.update()
                return

            if self.dataframe.shape[1] < 2:
                print("❌ Error: El CSV no tiene suficientes columnas.")
                self.page.snack_bar = ft.SnackBar(ft.Text("CSV file must have at least two columns"), open=True)
                self.page.update()
                return

            # Eliminar filas donde codigo_inicial esté vacío
            self.dataframe = self.dataframe.dropna(subset=[self.dataframe.columns[1]])

            # Volver a verificar que sigue habiendo datos después de limpiar
            if self.dataframe.empty:
                print("❌ Error: No hay datos válidos después de limpiar el DataFrame.")
                self.page.snack_bar = ft.SnackBar(ft.Text("No valid data after cleanup"), open=True)
                self.page.update()
                return

            # Crear diccionario de búsqueda y reemplazo
            replace_dict = {
                str(v).strip().upper(): str(k).strip()
                for k, v in zip(self.dataframe.iloc[:, 0], self.dataframe.iloc[:, 1])
            }
            print(f"🔍 Diccionario de reemplazo creado: {replace_dict}")

            doc = ezdxf.readfile(file_path)
            cambios_realizados = 0

            # 🔹 MODIFICAR NOMBRES DE CAPAS
            for layer in doc.layers:
                layer_name = layer.dxf.name.strip().upper()
                if layer_name in replace_dict:
                    new_value = replace_dict[layer_name]
                    print(f"Reemplazando capa: {layer_name} -> {new_value}")
                    layer.dxf.name = new_value  # Cambiar el nombre de la capa
                    cambios_realizados += 1

            # 🔹 MODIFICAR CAPAS EN ENTIDADES
            for entity in doc.entities:
                old_layer = entity.dxf.layer.upper()
                if old_layer in replace_dict:
                    entity.dxf.layer = replace_dict[old_layer]
                    print(f"Reemplazado en entidad: {old_layer} -> {entity.dxf.layer}")
                    cambios_realizados += 1

            # 🔹 MODIFICAR CAPAS EN BLOQUES
            for block in doc.blocks:
                for entity in block:
                    old_layer = entity.dxf.layer.upper()
                    if old_layer in replace_dict:
                        entity.dxf.layer = replace_dict[old_layer]
                        print(f"Reemplazado en bloque: {old_layer} -> {entity.dxf.layer}")
                        cambios_realizados += 1

            # Guardar el archivo solo si hubo cambios
            if cambios_realizados > 0:
                modified_file_path = file_path.replace(".dxf", "_modified.dxf")
                doc.saveas(modified_file_path)
                print(f"✅ DXF modificado guardado en {modified_file_path} ({cambios_realizados} cambios)")
                self.page.snack_bar = ft.SnackBar(ft.Text(f"DXF modificado guardado ({cambios_realizados} cambios)"), open=True)
            else:
                print("⚠️ No se encontraron coincidencias en el DXF")
                self.page.snack_bar = ft.SnackBar(ft.Text("No se encontraron coincidencias en el DXF"), open=True)

            self.page.update()

        except Exception as ex:
            print(f"❌ Error en modify_dxf: {str(ex)}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error modificando DXF: {str(ex)}"), open=True)
            self.page.update()


