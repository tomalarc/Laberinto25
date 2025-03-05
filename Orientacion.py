from ElementoMapa import *
class Orientacion:
    def __init__(self):
        self.nombre="Orientacion"
        pass

    def obtenerElementoOrEn(self, unContenedor):
        pass

    def ponerElemento(self, unEm, unContenedor):
        pass

class Norte(Orientacion):
    def __init__(self):
        super().__init__()
        self.nombre = "Norte"
    def ponerElemento(self, em, unContenedor):
        unContenedor.norte = em

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.norte

class Sur(Orientacion):
    def __init__(self):
        super().__init__()
        self.nombre = "Sur"
    def ponerElemento(self, em, unContenedor):
        unContenedor.sur = em

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.sur

class Este(Orientacion):
    def __init__(self):
        super().__init__()
        self.nombre = "Este"
    def ponerElemento(self, em, unContenedor):
        unContenedor.este = em

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.este

class Oeste(Orientacion):
    def __init__(self):
        super().__init__()
        self.nombre = "Oeste"
    def ponerElemento(self, em, unContenedor):
        unContenedor.oeste = em

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.oeste