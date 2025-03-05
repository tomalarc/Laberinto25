from Creators import *


class Juego:
    def __init__(self):
        self.creator = Creator()
        self.laberinto = self.creator.fabricarLaberinto(None)
        self.bichos = []

    #Por el momento se estan haciendo pruebas con el laberinto de 2 habitaciones y 2 bichos
    def crearLaberinto2Hab2Bichos(self):
        self.bichos.clear()
        self.laberinto.vaciarLaberinto()

        hab1 = self.creator.fabricarHabitacion(1)
        hab2 = self.creator.fabricarHabitacion(2)

        puerta = self.creator.fabricarPuerta(hab1, hab2, None)

        hab1.ponerEnOr(Oeste(), puerta)
        hab2.ponerEnOr(Este(), puerta)

        bicho1 = self.creator.fabricarBichoAgresivo(hab1)
        bicho2 = self.creator.fabricarBichoPerezoso(hab2)

        self.bichos.append(bicho1)
        self.bichos.append(bicho2)

        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)
        
