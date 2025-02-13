import flet as ft
import pandas as pd
from models import csv_reader as rd
from models import dataframe_viewer as dv
from models import code_container as cc
from models import modifier_container as mc


def main(page: ft.Page):
    page.title = "DXF Modifier"
    page.scroll = "adaptive"
    
    # Agregar la vista del DataFrame con botón
    page.add(
        ft.Row(
            controls=[
                cc.CodeContainer(),
                mc.ModifierContainer(page),
            ],
            alignment=ft.MainAxisAlignment.START
        )
    )

ft.app(target=main)