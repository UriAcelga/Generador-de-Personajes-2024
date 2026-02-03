import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
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

    def print_mediabox(self):
        box = self.reader.pages[0].mediabox
        print(f"Ancho: {box.width}, Alto: {box.height}")

    def get_campos_dict(self):
        # La posición del arreglo indica la página
        # en PDF (0,0) está en la esquina inferior izquierda
        # Se saben las coordenadas usando https://pdf-cordinate-extractor.vercel.app/
        # restar 8 a la coordenada Y

        return [
            {
                # --- ENCABEZADO (Página 1) ---
                "NOMBRE_PERSONAJE": {"text": "Grog", "pos": (40, 746, 200, 14), "size": 14},
                "TRASFONDO": {"text": "Soldado", "pos": (40, 724, 100, 11), "size": 11},
                "CLASE": {"text": "Bárbaro", "pos": (155, 724, 100, 11), "size": 11},
                "ESPECIE": {"text": "Semiorco", "pos": (40, 703, 100, 11), "size": 11},
                "SUBCLASE": {"text": "Berserker", "pos": (155, 703, 100, 11), "size": 11},
                "NIVEL": {"text": "3", "pos": (270, 729, 30, 16), "size": 16},
                "CA": {"text": "18", "pos": (325, 714, 40, 20), "size": 20},
                "HP_MAX": {"text": "35", "pos": (450, 704, 30, 10), "size": 10},
                "DADOS_GOLPE_MAX": {"text": "1d12", "pos": (502, 704, 40, 10), "size": 10},
                
                # --- COMBATE Y ARMAS (Página 1) ---
                "INICIATIVA": {"text": "+2", "pos": (255, 626, 40, 16), "size": 16},
                "VELOCIDAD": {"text": "30", "pos": (350, 626, 40, 16), "size": 16},

                "ARMA_1_NOMBRE": {"text": "Gran Hacha", "pos": (240, 562, 100, 9), "size": 9},
                "ARMA_1_BONIF": {"text": "+6", "pos": (350, 562, 30, 9), "size": 9},
                "ARMA_1_DAÑO": {"text": "1d12 cortante", "pos": (390, 562, 70, 8), "size": 8},
                "ARMA_1_NOTAS": {"text": "", "pos": (470, 562, 120, 8), "size": 8},
                
                "ARMA_2_NOMBRE": {"text": "Jabalina", "pos": (240, 542, 100, 9), "size": 9},
                "ARMA_2_BONIF": {"text": "+6", "pos": (350, 542, 30, 9), "size": 9},
                "ARMA_2_DAÑO": {"text": "1d6 perforante", "pos": (390, 542, 70, 8), "size": 8},
                "ARMA_2_NOTAS": {"text": "arrojable", "pos": (470, 542, 120, 8), "size": 8},

                # --- ATRIBUTOS (Página 1) ---
                "COMPETENCIA": {"text": "+2", "pos": (44, 607, 40, 22), "size": 22},
                "FUERZA_MOD": {"text": "+4", "pos": (28, 540, 40, 22), "size": 22},
                "FUERZA_SCORE": {"text": "18", "pos": (68, 540, 20, 10), "size": 10},
                "FUERZA_SAVE": {"text": "+6", "pos": (29, 507, 20, 9), "size": 9},

                "DESTREZA_MOD": {"text": "+2", "pos": (28, 422, 40, 22), "size": 22},
                "DESTREZA_SCORE": {"text": "14", "pos": (68, 422, 20, 10), "size": 10},
                "DESTREZA_SAVE": {"text": "+2", "pos": (29, 389, 20, 9), "size": 9},

                "CONSTITUCION_MOD": {"text": "+3", "pos": (28, 276, 40, 22), "size": 22},
                "CONSTITUCION_SCORE": {"text": "16", "pos": (68, 276, 20, 10), "size": 10},
                "CONSTITUCION_SAVE": {"text": "+3", "pos": (29, 243, 20, 9), "size": 9},

                "INTELIGENCIA_MOD": {"text": "-1", "pos": (138, 620, 40, 22), "size": 22},
                "INTELIGENCIA_SCORE": {"text": "8", "pos": (178, 620, 20, 10), "size": 10},
                "INTELIGENCIA_SAVE": {"text": "-1", "pos": (139, 584, 20, 9), "size": 9},

                "SABIDURIA_MOD": {"text": "+1", "pos": (138, 444, 40, 22), "size": 22},
                "SABIDURIA_SCORE": {"text": "12", "pos": (178, 444, 20, 10), "size": 10},
                "SABIDURIA_SAVE": {"text": "+1", "pos": (139, 411, 20, 9), "size": 9},

                "CARISMA_MOD": {"text": "+0", "pos": (138, 270, 40, 22), "size": 22},
                "CARISMA_SCORE": {"text": "10", "pos": (178, 270, 20, 10), "size": 10},
                "CARISMA_SAVE": {"text": "+0", "pos": (139, 237, 20, 9), "size": 9},

                # --- HABILIDADES ---
                "ATLETISMO": {"text": "+6", "pos": (29, 487, 20, 9), "size": 9},

                "ACROBACIAS": {"text": "+2", "pos": (29, 370, 20, 9), "size": 9},
                "JUEGO_DE_MANOS": {"text": "+2", "pos": (29, 356, 20, 9), "size": 9},
                "SIGILO": {"text": "+2", "pos": (29, 342, 20, 9), "size": 9},

                "CONOCIMIENTO_ARCANO": {"text": "+1", "pos": (139, 564, 20, 9), "size": 9},
                "HISTORIA": {"text": "+1", "pos": (139, 550, 20, 9), "size": 9},
                "INVESTIGACION": {"text": "+1", "pos": (139, 536, 20, 9), "size": 9},
                "NATURALEZA": {"text": "+1", "pos": (139, 522, 20, 9), "size": 9},
                "RELIGION": {"text": "+1", "pos": (139, 508, 20, 9), "size": 9},

                "MEDICINA": {"text": "+1", "pos": (139, 391, 20, 9), "size": 9},
                "PERCEPCION": {"text": "+3", "pos": (139, 377, 20, 9), "size": 9},
                "PERSPICACIA": {"text": "+1", "pos": (139, 363, 20, 9), "size": 9},
                "SUPERVIVENCIA": {"text": "+1", "pos": (139, 349, 20, 9), "size": 9},
                "TRATO_CON_ANIMALES": {"text": "+1", "pos": (139, 335, 20, 9), "size": 9},

                "ENGAÑO": {"text": "+2", "pos": (139, 217, 20, 9), "size": 9},
                "INTERPRETACION": {"text": "+2", "pos": (139, 203, 20, 9), "size": 9},
                "INTIMIDACION": {"text": "+2", "pos": (139, 189, 20, 9), "size": 9},
                "PERSUASION": {"text": "+2", "pos": (139, 175, 20, 9), "size": 9},
            },
            {
                # --- MAGIA (Página 2) ---
                "APTITUD": {"text": "WIS", "pos": (72, 742, 30, 14), "size": 14},
                "APTITUD_MOD": {"text": "+1", "pos": (21, 709, 30, 14), "size": 14},
                "CD DE SALVACION DE CONJUROS": {"text": "12", "pos": (21, 681, 30, 14), "size": 14},
                "BONIFICADOR DE ATAQUE DE CONJUROS": {"text": "+5", "pos": (21, 653, 30, 14), "size": 14},
                "ESPACIOS_NIVEL_1_TOTAL": {"text": "4", "pos": (187, 681, 20, 8), "size": 8},
                "ESPACIOS_NIVEL_2_TOTAL": {"text": "2", "pos": (187, 667, 20, 8), "size": 8},

                # --- EQUIPO Y MONEDAS (Página 2) ---
                "EQUIPO_LISTA": {"text": "Cota de malla, Espada larga, Escudo, Pack de explorador", "pos": (410, 150, 150, 100), "size": 11},
                "MONEDAS_PC": {"text": "25", "pos": (420, 52, 30, 11), "size": 11},
                "MONEDAS_PP": {"text": "25", "pos": (457, 52, 30, 11), "size": 11},
                "MONEDAS_PO": {"text": "110", "pos": (527, 52, 30, 11), "size": 11},

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
        estiloBase = ParagraphStyle(
            name="base",
            fontName="Helvetica",
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            spaceBefore=0,
            spaceAfter=0,
        )
        for i in range(len(self.reader.pages)):
            for campo in self.CONFIG_CAMPOS[i].values():
                x, y, w, h = campo["pos"]
                estiloCampo = estiloBase.clone(
                    'temp',
                    fontSize=campo["size"],
                    leading=campo["size"],
                )
                p = Paragraph(campo["text"], estiloCampo)
                f = Frame(x, y, w, h, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary=0)
                f.addFromList([p], cv)
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

