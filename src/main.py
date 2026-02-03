import flet as ft
from flet import Colors
from pdfmanager import PdfManager


def main(page: ft.Page):


    status_text = ft.Text("Presiona el botón para editar el PDF modelo", size=16)
    


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
            page.snack_bar = ft.SnackBar(ft.Text("¡Proceso completado con éxito!"))
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

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                status_text,
                ft.IconButton(ft.Icons.ADD, on_click=gestionar_pdf),
            ],
        )
    )


ft.run(main)
