from Modo import *

class Bicho:
    def __init__(self, modo, posicion):
        self.vidas = 5
        self.poder = 1
        self.modo = modo
        self.posicion = posicion
        

    def esAgresivo(self):
        return self.modo.esAgresivo()
    
    def esPerezoso(self):
        return self.modo.esPerezoso()
    
    def esBoss(self):
        return self.modo.esBoss()

    def iniAgresivo(self):
        self.modo = Agresivo()
        self.poder = 10
        self.vidas = 5

    def iniPerezoso(self):
        self.modo = Perezoso()
        self.poder = 1
        self.vidas = 5

    def iniBoss(self):
        self.modo = Boss()
        self.poder = 20
        self.vidas = 10