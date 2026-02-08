class DndData:
    @staticmethod
    def get_clases():
        return [
            "Barbaro",
            "Bardo",
            "Brujo",
            "Clerigo",
            "Druida",
            "Explorador",
            "Guerrero",
            "Hechicero",
            "Mago",
            "Monje",
            "Paladin",
            "Picaro"
        ]
    
    @staticmethod
    def get_trasfondos():
        return {
            "Barbaro": ["Granjero", "Guía", "Soldado", "Marinero"],
            "Bardo": ["Charlatán", "Artista", "Noble", "Caminante"],
            "Brujo": ["Acólito", "Charlatán", "Ermitaño", "Mercader"],
            "Clerigo": ["Acólito", "Ermitaño", "Sabio", "Escribano"],
            "Druida": ["Guía", "Ermitaño", "Erudito", "Escribano", "Caminante"],
            "Explorador": ["Guía", "Criminal", "Caminante"],
            "Guerrero": ["Soldado", "Noble", "Guardia", "Granjero"],
            "Hechicero": ["Charlatán", "Ermitaño", "Sabio", "Acólito"],
            "Mago": ["Acólito", "Escribano", "Ermitaño", "Mercader"],
            "Monje": ["Guía", "Marinero"],
            "Paladin": ["Noble", "Soldado", "Acólito"],
            "Picaro": ["Criminal", "Charlatán", "Caminante"]
        }
    
    
    @staticmethod
    def get_trasfondos_segun_clase(clase):
        try:
            return DndData.get_trasfondos()[clase]
        except KeyError:
            return None