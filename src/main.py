import flet as ft
from flet import Colors
from pdfmanager import PdfManager
from personaje import Personaje


def Dropdown(default="Selecciona una opción", dp_label="Seleccion", opciones=["1", "2", "3"]):
    dp_opciones = [ft.DropdownOption(opcion) for opcion in opciones]
    def dp_on_change(e):
        print(f"Selección de clase: {e.control.value}")
        e.control.update()
        
    return ft.Dropdown(
        label=dp_label,
        options=dp_opciones,
        on_select=dp_on_change
    )

def Slider(label="Selección:", min=1, max=20):
    valor_slider = min
    slider_text = ft.Text(value=f"Valor actual: {valor_slider}")
    def cambiar_slider(e):
        valor_slider = int(e.control.value)
        slider_text.value = f"Valor actual: {valor_slider}"
        slider_text.update()

    return ft.Column(
            controls=[
                ft.Text(label),
                ft.Slider(
                    value=valor_slider,
                    min=min,
                    max=max,
                    divisions=max-min,
                    label="{value}",
                    on_change=cambiar_slider,
                ),
                slider_text,
            ]
        )



def main(page: ft.Page):

    status_text = ft.Text(
        "Presiona el botón para editar el PDF modelo", size=16)
    tiradas_text = ft.Text("Generar tiradas", size=16)

    def generar_personaje(e):
        data_pj = {"NVL": 3, "CLASE": "Guerrero"}
        pj = Personaje(data=data_pj)
        tiradas_text.value = f"✅ Tiradas: {pj.tiradas}"
        tiradas_text.color = ft.Colors.GREEN
        page.update()

    def gestionar_pdf(e):
        pdfm = PdfManager()
        print("Páginas:", pdfm.get_num_pages())
        pdfm.print_mediabox()
        if pdfm.get_status() == "OK":
            # 2. Aplicar anotación y guardar con timestamp
            path_resultado = pdfm.crear_anotaciones()
            status_text.value = f"✅ PDF guardado en: {path_resultado}"
            status_text.color = ft.Colors.GREEN

            # Notificación visual rápida
            page.snack_bar = ft.SnackBar(
                ft.Text("¡Proceso completado con éxito!"))
            page.snack_bar.open = True
            """try:
            except Exception as ex:
                status_text.value = f"❌ Error al guardar: {ex}"
                status_text.color = ft.Colors.RED"""
        else:
            status_text.value = "❌ No se encontró el pdf"
            status_text.color = ft.Colors.ORANGE
            print("Status:", pdfm.get_status())

        page.update()

    # Renderizado de componentes gráficos
    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                status_text,
                ft.IconButton(ft.Icons.ADD, on_click=gestionar_pdf),
            ],
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                tiradas_text,
                ft.IconButton(ft.Icons.ADD, on_click=generar_personaje),
            ],
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                Dropdown(dp_label="Clase:", opciones=["barbaro", "mago", "paladin"]),
                ft.TextField(
                    label="Nombre de personaje",
                    hint_text="Gandalf",
                    expand=True
                ),
            ]
        ),
        ft.Column(
            Slider(label="Nivel:", min=1, max=20)
        ),

        
    )


ft.run(main)
