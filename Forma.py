from Orientacion import *
import random


class Forma:
    def __init__(self):
        self.orientaciones = []

    
    def agregarOrientacion(self, orientacion):
        if orientacion not in self.orientaciones:
            
            self.orientaciones.append(orientacion)
    def obtenerElementoOR(self, orientacion):
        return orientacion.obtenerElementoOrEn(self)
    def obtenerOrientacion(self):
        ori = random.choice(self.orientaciones)
        return ori
    def obtenerOrientaciones(self):
        return self.orientaciones
    def ponerEnOrientacion(self, orientacion, elemMapa):
        orientacion.ponerElemento(elemMapa, self)

class Cuadrado(Forma):
    def __init__(self):
        super().__init__()
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None
    
    def irNorte(self, alguien):
        if self.norte is not None:
            self.norte.entrar(alguien)
        else:
            print(alguien.nombre, " Intenta entrar en un norte vacío")
    def irSur(self, alguien):
        if self.sur is not None:
            self.sur.entrar(alguien)
        else:
            print(alguien.nombre, " Intenta entrar en un sur vacío")
    def irEste(self, alguien):
        if self.este is not None:
            self.este.entrar(alguien)
        else:
            print(alguien.nombre, " Intenta entrar en un este vacío")
    def irOeste(self, alguien):
        if self.oeste is not None:
            self.oeste.entrar(alguien)
        else:
            print(alguien.nombre, " Intenta entrar en un oeste vacío")

class Rombo(Forma):
    def __init__(self):
        super().__init__()
        self.noreste = None
        self.sureste = None
        self.noroeste = None
        self.suroeste = None

    def irNoreste(self, alguien):
        if self.noreste is not None:
            self.noreste.entrar(alguien)
        else:
            print(alguien.nombre, " Intenta entrar en un noreste vacío")

    def irNoroeste(self, alguien):
        if self.noroeste is not None:
            self.noroeste.entrar(alguien)
        else:
            print(alguien.nombre, " Intenta entrar en un noroeste vacío")
    
    def irSureste(self, alguien):
        if self.sureste is not None:
            self.sureste.entrar(alguien)
        else:
            print(alguien.nombre, " Intenta entrar en un sureste vacío")

    def irSuroeste(self, alguien):
        if self.suroeste is not None:
            self.suroeste.entrar(alguien)
        else:
            print(alguien.nombre, " Intenta entrar en un suroeste vacío")