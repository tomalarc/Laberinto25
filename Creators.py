from ElementoMapa import *
from Orientacion import *
from Modo import *
from Forma import *
from Comando import *
from Entes import *

class Creator:
    def __init__(self):
        pass
    
    
    def fabricarPared(self, padre=None):
        return Pared(padre)

    def fabricarPuerta(self, lado1, lado2, padre=None):
        return Puerta(lado1, lado2, padre)

    def fabricarHabitacion(self, num, padre=None):
        hab = Habitación(padre)
        hab.forma=Cuadrado()
        hab.num = num
        hab.agregarOrientacion(self.fabricarNorte())
        hab.agregarOrientacion(self.fabricarSur())
        hab.agregarOrientacion(self.fabricarEste())
        hab.agregarOrientacion(self.fabricarOeste())

        for orientacion in hab.forma.orientaciones:
            pared = self.fabricarPared()
            hab.ponerEnOrientacion(orientacion, pared)
        return hab

    def fabricarLaberintoVacio(self, padre=None):
        return Laberinto(padre)
    
    def fabricarBomba(self,em):
        return Bomba(em)
    
    def cambiarAModoAgresivo(self, bicho):
        bicho.modo = Agresivo()
        bicho.poder = 10
    
    def fabricarBichoAgresivo(self, unaHab):
        bicho = Bicho()
        bicho.iniAgresivo()
        bicho.posicion = unaHab
        return bicho
    
    def fabricarBichoPerezoso(self, unaHab):
        bicho = Bicho()
        bicho.iniPerezoso()
        bicho.posicion = unaHab
        return bicho
    
    def fabricarPersonaje(self, nombre):
        return Player(nombre)

    
    
    #Aplicar singleton:
    def fabricarNorte(self):
        return Norte()
    
    def fabricarSur(self):
        return Sur()
    
    def fabricarEste(self):
        return Este()
    
    def fabricarOeste(self):
        return Oeste()

class CreatorBomba(Creator):
    def __init__(self):
        super().__init__()
    
    def fabricarPared(self, padre):
        return ParedBomba(padre)