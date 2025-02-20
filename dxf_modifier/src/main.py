import flet as ft
from models import csv_reader as rd
from models import code_container as cc
from models import modifier_container as mc

def main(page: ft.Page):
    page.title = "DXF Modifier"
    page.scroll = "adaptive"


    csv_reader = rd.CSVReader()  
    
    page.add(
        ft.Row(
            controls=[
                cc.CodeContainer(page, csv_reader),
                mc.ModifierContainer(page, csv_reader), 
            ],
            alignment=ft.MainAxisAlignment.START
        )
    )

ft.app(target=main)
