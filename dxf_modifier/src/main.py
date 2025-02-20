import flet as ft
from models import csv_reader as rd
from models import code_container as cc
from models import modifier_container as mc
from models import posible_new_layers as pnl

def main(page: ft.Page):
    page.title = "DXF Modifier"
    page.scroll = "adaptive"
    
    logo_path = "dxf_modifier/src/assets/logo.png"

    csv_reader = rd.CSVReader()
    code_container = cc.CodeContainer(page, csv_reader)
    
    logo_container = ft.Container(
        content=ft.Image(src=logo_path, width=300, height=100),  # Imagen del logo
        width=400,  # Ancho fijo para evitar que se mueva con la ventana
        alignment=ft.alignment.top_center,  # Lo mantiene fijo en el centro
        padding=ft.padding.only(top=20, bottom=20),
        margin=ft.margin.only(left=200)
    )

    # Crear una función de actualización
    def update_layers():
        posible_new_layers.new_layers_column.controls.clear()
        modifier_container.not_modified_layers.sort()
        for layer in modifier_container.not_modified_layers:
            tfield_layer = ft.TextField(label="Layer Name", width="100%", text_size=24, value=layer, read_only=True)
            tfield_new_code = ft.TextField(label="New Layer Name", width="100%", text_size=24, max_length=6)

            button = ft.ElevatedButton(
                "Add Layer", 
                on_click=lambda e, l=tfield_layer, n=tfield_new_code: posible_new_layers.write_on_csv(e, l, n)
            )
            posible_new_layers.new_layers_column.controls.append(ft.Row([tfield_layer, tfield_new_code, button]))

        posible_new_layers.page.update()

    modifier_container = mc.ModifierContainer(page, csv_reader, update_layers)
    posible_new_layers = pnl.PosibleNewLayers(page, csv_reader, modifier_container)
    
    page.add(
        ft.Column(
            controls=[
                logo_container,  # Se coloca el logo en la parte superior
                ft.Container(  # Desplaza los contenedores amarillos hacia abajo
                    content=ft.Row(
                        controls=[code_container, modifier_container],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    padding=ft.margin.only(left=230) # Ajusta la cantidad para bajarlos
                ),
                posible_new_layers  # Ahora estarán alineados
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
    )


ft.app(target=main)

