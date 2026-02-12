class DndData:
    @staticmethod
    def clases():
        return [
            "Bárbaro",
            "Bardo",
            "Brujo",
            "Clérigo",
            "Druida",
            "Explorador",
            "Guerrero",
            "Hechicero",
            "Mago",
            "Monje",
            "Paladín",
            "Pícaro"
        ]
    
    @staticmethod
    def razas():
        return [
            "Aasimar"
            "Dracónido", 
            "Elfo", 
            "Enano", 
            "Gnomo", 
            "Goliat", 
            "Humano", 
            "Mediano", 
            "Orco", 
            "Tiefling"
        ]

    @staticmethod
    def trasfondos():
        return [
            "Acólito",
            "Animador",
            "Artesano",
            "Campesino",
            "Charlatán",
            "Comerciante",
            "Criminal",
            "Ermitaño",
            "Erudito",
            "Escriba",
            "Guardia",
            "Guía",
            "Marinero",
            "Noble",
            "Soldado",
            "Vagabundo"

        ]        
    
    @staticmethod
    def trasfondos_por_clase():
        return {
            "Barbaro": ["Campesino", "Guía", "Soldado", "Marinero"],
            "Bardo": ["Charlatán", "Animador", "Noble", "Vagabundo"],
            "Brujo": ["Acólito", "Charlatán", "Ermitaño", "Comerciante"],
            "Clerigo": ["Acólito", "Ermitaño", "Erudito", "Escriba"],
            "Druida": ["Guía", "Ermitaño", "Erudito", "Escriba", "Vagabundo"],
            "Explorador": ["Guía", "Criminal", "Vagabundo"],
            "Guerrero": ["Soldado", "Noble", "Guardia", "Campesino"],
            "Hechicero": ["Charlatán", "Ermitaño", "Erudito", "Acólito"],
            "Mago": ["Acólito", "Escriba", "Ermitaño", "Comerciante"],
            "Monje": ["Guía", "Marinero"],
            "Paladin": ["Noble", "Soldado", "Acólito"],
            "Picaro": ["Criminal", "Charlatán", "Vagabundo"]
        }
    
    
    @staticmethod
    def get_trasfondos_segun_clase(clase):
        try:
            return DndData.get_trasfondos()[clase]
        except KeyError:
            return None