import numpy as np

"""
personaje = {
    "STR": 12,
    "DEX": 12,
    "CON": 12,
    "INT": 12,
    "WIS": 12,
    "CHR": 12,
    
    "clase": "Guerrero",
    "subclase": "Guerrero Arcano",
    "especie": "Humano",
    "trasfondo": "Charlatan",

    "nvl": 3,
    "competencia": 2,
    "hp": 31,

    "CA": 16,

    "HAB_COMPETENCIAS": [],
    "HAB_MAESTRIAS": [],
    "iniciativa": 1,
    "velocidad": 30,

    "atletismo": 3,

    "acrobacias": 3,
    "juego_de_manos": 3,
    "sigilo": 3,

    "conocimiento_arcano": 3,
    "historia": 3,
    "investigacion": 3,
    "naturaleza": 3,
    "religion": 3,

    "medicina": 3,
    "percepcion": 3,
    "perspicacia": 3,
    "supervivencia": 3,
    "trato_con_animales": 3,

    "engaño": 3,
    "interpretacion": 3,
    "intimidacion": 3,
    "persuasion": 3,

    "aptitud": "INT",
    "CD_salvacion": 12,
    "bonif_ataque": 5,
    "espacios_nvl_1": 3,
    "espacios_nvl_2": 1,
    "espacios_nvl_3": 0,
    "espacios_nvl_4": 0,
    "espacios_nvl_5": 0,
    "espacios_nvl_6": 0,
    "espacios_nvl_7": 0,
    "espacios_nvl_8": 0,

    "ARMAS": [
        {
            "nombre": "Gran_Hacha",
            "daño": "1d12",
            "tipo_daño": "cortante",
            "maestria": "debilitar",
            "caracteristicas": ["gran_alcance", "arrojadiza"],
        }
        {
            "nombre": "Gran_Hacha",
            "daño": "1d12",
            "tipo_daño": "cortante",
            "maestria": "debilitar",
            "caracteristicas": ["gran_alcance", "arrojadiza"],
        }
    ],

}
"""

class Personaje:
    def __init__(self, data):
        #Utilidades
        self.rng = np.random.default_rng()

        #Características esenciales
        self.NVL = data["NVL"]
        self.CLASE = data["CLASE"]

        #Datos que dependen del nivel
        self.COMPETENCIA = None
        self.calcular_bonif_competencia()

        #Clase
        self.SUBCLASE = None

        #Datos que dependen de la Clase
        self.ESPECIE = None
        self.TRASFONDO = None

        #Características
        self.STR = None
        self.DEX = None
        self.CON = None
        self.INT = None
        self.WIS = None
        self.CHR = None
        self.tiradas = self.generar_tiradas()
        
        
        


        #Datos que dependen de las características
        self.INICIATIVA = None
        self.HP = None
        self.CA = None


    def calcular_bonif_competencia(self):
        self.COMPETENCIA = 1 + int(-(-(0.25 * self.NVL) // 1))

    def generar_tiradas(self):
        print("Generando tiradas...")
        tiradas = []
        for i in range(6):
            print(f"Tirando stat n°{i+1}")
            rerolls = 2
            stat = []
            for j in range(4):
                n = self.rng.integers(low=1, high=6, endpoint=True)
                print(f"Roll n°{j+1} de stat n°{i+1}: {n}")
                while n <= 2 and rerolls > 0:
                    rerolls -= 1
                    print(f"Rerolleando {n} ({rerolls} rerolls disponibles)...")
                    n = self.rng.integers(low=1, high=6, endpoint=True)
                    print(f"Roll n°{j+1} de stat n°{i+1}: {n}")
                stat.append(n)
            tirada = sum(sorted(stat)[1:]).item()
            print(f"Rolls de Stat n°{i+1}: {stat} - Resultado: {tirada}")
            tiradas.append(tirada)
        print(f"Tiradas finalizadas - Resultado: {tiradas}")
        return tiradas


    #Pasar estos datos relacionados a otra clase????
    def get_trasfondos():
        return {
            "barbaro": ["Granjero", "Guía", "Soldado", "Marinero"],
            "bardo": ["Charlatán", "Artista", "Noble", "Caminante"],
            "brujo": ["Acólito", "Charlatán", "Ermitaño", "Mercader"],
            "clerigo": ["Acólito", "Ermitaño", "Sabio", "Escribano"],
            "druida": ["Guía", "Ermitaño", "Erudito", "Escribano", "Caminante"],
            "explorador": ["Guía", "Criminal", "Caminante"],
            "guerrero": ["Soldado", "Noble", "Guardia", "Granjero"],
            "hechicero": ["Charlatán", "Ermitaño", "Sabio", "Acólito"],
            "mago": ["Acólito", "Escribano", "Ermitaño", "Mercader"],
            "monje": ["Guía", "Marinero"],
            "paladin": ["Noble", "Soldado", "Acólito"],
            "picaro": ["Criminal", "Charlatán", "Caminante"]
        }
    
    def get_clases():
        return [
            "barbaro",
            "bardo",
            "brujo",
            "clerigo",
            "druida",
            "explorador",
            "guerrero",
            "hechicero",
            "mago",
            "monje",
            "paladin",
            "picaro"
        ]
    
    def get_trasfondos_segun_clase(self, clase):
        return self.get_trasfondos()[clase]
    
    def generar_trasfondo(self):
        trasfondos = self.get_trasfondos_segun_clase(self.CLASE)
        i = self.rng.integers(low=0, high=len(trasfondos)).item()
        return trasfondos[i]






