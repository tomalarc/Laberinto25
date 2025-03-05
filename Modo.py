class Modo:
    def __init__(self):
        pass

    def actua(self, unBicho):
        self.camina(unBicho)

    def camina(self, unBicho):
        "self subclassResponsibility."
        "definir un caminar predeterminado"

    def esAgresivo(self):
        return False
    
    def esPerezoso(self):
        return False
    
    def esBoss(self):
        return False

class Agresivo(Modo):
    def __init__(self):
        super().__init__()

    def esAgresivo(self):
        return True

class Perezoso(Modo):
    def __init__(self):
        super().__init__()

    def esPerezoso(self):
        return True
    
class Boss(Modo):
    def __init__(self):
        super().__init__()

    def esBoss(self):
        return True
