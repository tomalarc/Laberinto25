from ElementoMapa import *
from Orientacion import *
from Modo import *
from Bicho import *

class Creator:
    def __init__(self):
        pass

    def fabricarPared(self):
        return Pared()

    def fabricarPuerta(self, lado1, lado2, padre):
        return Puerta(lado1, lado2, padre)

    def fabricarHabitacion(self, num):
        hab = Habitación(num)
        hab.agregarOrientacion(Norte())
        hab.agregarOrientacion(Sur())
        hab.agregarOrientacion(Este())
        hab.agregarOrientacion(Oeste())

        for orientacion in hab.orientaciones:
            hab.ponerEnOr(orientacion, self.fabricarPared())
        
        return hab

    def fabricarLaberinto(self, padre):
        return Laberinto(padre)
    
    def fabricarBomba(self,em):
        return Bomba(em)
    
    def cambiarAModoAgresivo(self, bicho):
        bicho.modo = Agresivo()
        bicho.poder = 5
    
    def fabricarBichoAgresivo(self, unaHab):
        bicho = Bicho(Agresivo(), unaHab)
        bicho.vidas = 5
        bicho.poder = 5
        return bicho
    
    def fabricarBichoPerezoso(self, unaHab):
        bicho = Bicho(Perezoso(), unaHab)
        bicho.vidas = 1
        bicho.poder = 1
        return bicho
    
    def fabricarBoss(self, unaHab):
        bicho = Bicho(Boss(), unaHab)
        bicho.vidas = 10
        bicho.poder = 20
        return bicho
    
    def fabricarNorte(self):
        return Norte()
    
    def fabricarSur(self):
        return Sur()
    
    def fabricarEste(self):
        return Este()
    
    def fabricarOeste(self):
        return Oeste()
