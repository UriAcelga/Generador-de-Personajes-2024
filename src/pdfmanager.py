import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pathlib import Path
from datetime import datetime

class PdfManager:
    def __init__(self, filename="charsheet2024.pdf"):
        self.CONFIG_CAMPOS = self.get_campos_dict()
        self.base_path = Path(__file__).resolve().parent / "assets"
        self.pdf_path = self.base_path / filename
        self.result_path = self.base_path / "personajes"
        self.reader = None
        self.writer = None
        self.status = "UNLOADED"
        self.cargar_template()
        self.cargar_writer()

    def get_num_pages(self):
        self.reader.get_num_pages()

    def get_campos_dict(self):
        # La posición del arreglo indica la página
        # en PDF (0,0) está en la esquina inferior izquierda
        # Se saben las coordenadas usando https://pdf-cordinate-extractor.vercel.app/
        """return [
            {
                "nombre": {"text": "Manolo", "pos": (40, 754, 210, 12)}
                "trasfondo": {"text": "Vagabundo", "pos": (40, 732, 105, 12)}
                "clase": {"text": "Guerrero", "pos": (155, 732, 90, 12)}
                "especie": {"text": "Humano", "pos": (40, 711, 105, 12)}
                "subclase": {"text": "Maestro de Combate", "pos": (155, 711, 90, 12)}

                "nivel": {"text": "5", "pos": (270, 737, 20, 20)}
                "CA": {"text": "18", "pos": (335, 722, 20, 43)}

            }
        ]"""

        return [
            {
                # --- ENCABEZADO (Página 1) ---
                "NOMBRE_PERSONAJE": {"text": "Grog", "x": 30, "y": 735, "size": 14},
                "CLASE": {"text": "Bárbaro", "x": 155, "y": 715, "size": 11},
                "TRASFONDO": {"text": "Soldado", "x": 30, "y": 715, "size": 11},
                "ESPECIE": {"text": "Semiorco", "x": 30, "y": 695, "size": 11},
                "SUBCLASE": {"text": "Berserker", "x": 135, "y": 695, "size": 11},
                "NIVEL": {"text": "3", "x": 245, "y": 715, "size": 11},
                "PX": {"text": "900", "x": 245, "y": 695, "size": 11},

                # --- ATRIBUTOS Y SALVACIONES (Página 1) ---
                # Formato: MODIFICADOR (Grande), PUNTUACIÓN (Pequeño), SALVACIÓN (Marcador)
                "FUERZA_MOD": {"text": "+4", "x": 28, "y": 528, "size": 22},
                "FUERZA_SCORE": {"text": "18", "x": 58, "y": 532, "size": 10},
                "FUERZA_SAVE": {"text": "+6", "x": 58, "y": 503, "size": 9},

                "DESTREZA_MOD": {"text": "+2", "x": 28, "y": 410, "size": 22},
                "DESTREZA_SCORE": {"text": "14", "x": 58, "y": 414, "size": 10},
                "DESTREZA_SAVE": {"text": "+2", "x": 58, "y": 385, "size": 9},

                "CONSTITUCION_MOD": {"text": "+3", "x": 28, "y": 264, "size": 22},
                "CONSTITUCION_SCORE": {"text": "16", "x": 58, "y": 268, "size": 10},
                "CONSTITUCION_SAVE": {"text": "+3", "x": 58, "y": 239, "size": 9},

                "INTELIGENCIA_MOD": {"text": "-1", "x": 132, "y": 604, "size": 22},
                "INTELIGENCIA_SCORE": {"text": "8", "x": 162, "y": 608, "size": 10},
                "INTELIGENCIA_SAVE": {"text": "-1", "x": 162, "y": 579, "size": 9},

                "SABIDURIA_MOD": {"text": "+1", "x": 132, "y": 432, "size": 22},
                "SABIDURIA_SCORE": {"text": "12", "x": 162, "y": 436, "size": 10},
                "SABIDURIA_SAVE": {"text": "+1", "x": 162, "y": 407, "size": 9},

                "CARISMA_MOD": {"text": "+0", "x": 132, "y": 258, "size": 22},
                "CARISMA_SCORE": {"text": "10", "x": 162, "y": 262, "size": 10},
                "CARISMA_SAVE": {"text": "+0", "x": 162, "y": 233, "size": 9},

                # --- HABILIDADES (Página 1 - Columna Izquierda/Centro) ---
                "ATLETISMO": {"text": "+6", "x": 58, "y": 489, "size": 8},
                "ACROBACIAS": {"text": "+2", "x": 58, "y": 371, "size": 8},
                "SIGILO": {"text": "+2", "x": 58, "y": 343, "size": 8},
                "MEDICINA": {"text": "+1", "x": 162, "y": 393, "size": 8},
                "PERCEPCION": {"text": "+3", "x": 162, "y": 379, "size": 8},
                "PERSPICACIA": {"text": "+1", "x": 162, "y": 365, "size": 8},
                "INTIMIDACION": {"text": "+2", "x": 162, "y": 182, "size": 8},

                # --- COMBATE Y VIDA (Página 1) ---
                "CA": {"text": "15", "x": 315, "y": 715, "size": 20},
                "INICIATIVA": {"text": "+2", "x": 185, "y": 665, "size": 16},
                "VELOCIDAD": {"text": "30", "x": 245, "y": 665, "size": 16},
                "HP_MAX": {"text": "35", "x": 455, "y": 742, "size": 10},
                "HP_ACTUAL": {"text": "35", "x": 395, "y": 705, "size": 28},
                "HP_TEMP": {"text": "0", "x": 475, "y": 705, "size": 18},
                "DADOS_GOLPE_MAX": {"text": "3d12", "x": 515, "y": 742, "size": 9},
                "DADOS_GOLPE_ACTUAL": {"text": "3", "x": 490, "y": 715, "size": 14},

                # --- ARMAS (Página 1 - Sección central) ---
                "ARMA_1_NOMBRE": {"text": "Gran Hacha", "x": 230, "y": 560, "size": 9},
                "ARMA_1_BONIF": {"text": "+6", "x": 335, "y": 560, "size": 9},
                "ARMA_1_DAÑO": {"text": "1d12+4 C", "x": 370, "y": 560, "size": 9},
                
                "ARMA_2_NOMBRE": {"text": "Jabalina", "x": 230, "y": 545, "size": 9},
                "ARMA_2_BONIF": {"text": "+6", "x": 335, "y": 545, "size": 9},
                "ARMA_2_DAÑO": {"text": "1d6+4 P", "x": 370, "y": 545, "size": 9},
            },

            {
                # --- EQUIPO Y MONEDAS (Página 2) ---
                "MONEDAS_PO": {"text": "150", "x": 440, "y": 420, "size": 11},
                "MONEDAS_PP": {"text": "25", "x": 410, "y": 420, "size": 11},
                "EQUIPO_LISTA": {"text": "Cota de malla, Espada larga, Escudo, Pack de explorador", "x": 380, "y": 150, "size": 11},

                # --- MAGIA (Página 2) ---
                "CD DE SALVACION DE CONJUROS": {"text": "14", "x": 320, "y": 725, "size": 11},
                "BONIFICADOR DE ATAQUE DE CONJUROS": {"text": "+6", "x": 320, "y": 660, "size": 11},
                "ESPACIOS_NIVEL_1_TOTAL": {"text": "4", "x": 325, "y": 630, "size": 11},
                "ESPACIOS_NIVEL_2_TOTAL": {"text": "2", "x": 325, "y": 605, "size": 11},
            }
        ]

    def get_status(self):
        return self.status
    
    def cargar_template(self):
        try:
            self.reader = PdfReader(str(self.pdf_path))
            self.status = "OK"
        except Exception as e:
            print(f"Error al abrir PDF: {e}")
            self.status = "NOT_FOUND"

    def cargar_writer_con_paginas(self):
        self.writer = PdfWriter()
        for pag in self.reader.pages:
            self.writer.add_page(pag)

    def cargar_writer(self):
        self.writer = PdfWriter()

    def crear_anotaciones(self):
        packet = io.BytesIO()
        cv = canvas.Canvas(packet, pagesize=letter)
        for i in range(len(self.reader.pages)):
            for campo in self.CONFIG_CAMPOS[i].values():
                cv.setFont("Helvetica", campo["size"])
                cv.drawString(campo["x"], campo["y"], campo["text"])
            cv.showPage()
        
        cv.save() #guardar cambios
        packet.seek(0) 
        pdf_memoria = PdfReader(packet) #Nuevo reader temporal
    
        # Fusionar páginas
        for i in range(len(self.reader.pages)):
            self.reader.pages[i].merge_page(pdf_memoria.pages[i])
            self.writer.add_page(self.reader.pages[i])

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        result_filename = f"{timestamp}.pdf"
        with open(self.result_path / result_filename, "wb") as f:
            self.writer.write(f)   
        return str(self.result_path / result_filename)

