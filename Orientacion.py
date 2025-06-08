from ElementoMapa import *

class Orientacion:
    def __init__(self):
        self.nombre="Orientacion"
    
    def __str__(self):
        return self.nombre
    def caminar(self, unBicho):
        pass
    def obtenerElementoOrEn(self, unContenedor):
        pass

    def ponerElemento(self, elemMapa, unContenedor):
        pass
    def recorrer(self, unBloque, unContenedor):
        pass
    def esNorte(self):
        return False
    def esSur(self):
        return False
    def esEste(self):
        return False
    def esOeste(self):
        return False

#PARA EL CUADRADO
class Norte(Orientacion):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'nombre'):  # Evitar reinicialización
            super().__init__()
            self.nombre = "Norte"

    def esNorte(self):
        return True
    def caminar(self, unBicho):
        posicion = unBicho.posicion
        posicion.irNorte(unBicho)

    def recorrer(self, operacion, unContenedor, nivel=0, imprimir = False):
        if imprimir:
            print("   "*nivel, self, ": ", end=" ")
        unContenedor.forma.norte.recorrer(operacion)

    def ponerElemento(self, elemMapa, unContenedor):
        unContenedor.norte = elemMapa

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.forma.norte

class Sur(Orientacion):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'nombre'):
            super().__init__()
            self.nombre = "Sur"
    def esSur(self):
        return True
    def caminar(self, unBicho):
        posicion = unBicho.posicion
        posicion.irSur(unBicho)

    def recorrer(self, operacion, unContenedor, nivel=0, imprimir = False):
        if imprimir:
            print("   "*nivel, self, ": ", end=" ")
        unContenedor.forma.sur.recorrer(operacion)

    def ponerElemento(self, elemMapa, unContenedor):
        unContenedor.sur = elemMapa

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.forma.sur

class Este(Orientacion):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'nombre'):
            super().__init__()
            self.nombre = "Este"
    def esEste(self):
        return True
    def caminar(self, unBicho):
        posicion = unBicho.posicion
        posicion.irEste(unBicho)

    def recorrer(self, operacion, unContenedor, nivel=0, imprimir = False):
        if imprimir:
            print("   "*nivel, self, ": ", end=" ")
        unContenedor.forma.este.recorrer(operacion)

    def ponerElemento(self, elemMapa, unContenedor):
        unContenedor.este = elemMapa

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.forma.este

class Oeste(Orientacion):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'nombre'):
            super().__init__()
            self.nombre = "Oeste"
    def esOeste(self):
        return True
    def caminar(self, unBicho):
        posicion = unBicho.posicion
        posicion.irOeste(unBicho)

    def recorrer(self, operacion, unContenedor, nivel=0, imprimir = False):
        if imprimir:
            print("   "*nivel, self, ": ", end=" ")
        unContenedor.forma.oeste.recorrer(operacion)

    def ponerElemento(self, elemMapa, unContenedor):
        unContenedor.oeste = elemMapa

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.forma.oeste

#PARA EL ROMBO
class Noreste(Orientacion):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'nombre'):  # Evitar reinicialización
            super().__init__()
            self.nombre = "Noreste"

    def esNorte(self):
        return True
    def caminar(self, unBicho):
        posicion = unBicho.posicion
        posicion.irNoreste(unBicho)

    def recorrer(self, operacion, unContenedor, nivel=0, imprimir = False):
        if imprimir:
            print("   "*nivel, self, ": ", end=" ")
        unContenedor.forma.noreste.recorrer(operacion)

    def ponerElemento(self, elemMapa, unContenedor):
        unContenedor.noreste = elemMapa

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.forma.noreste

class Noroeste(Orientacion):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'nombre'):
            super().__init__()
            self.nombre = "Noroeste"

    def esNorte(self):
        return True
    def caminar(self, unBicho):
        posicion = unBicho.posicion
        posicion.irNoroeste(unBicho)

    def recorrer(self, operacion, unContenedor, nivel=0, imprimir=False):
        if imprimir:
            print("   "*nivel, self, ": ", end=" ")
        unContenedor.forma.noroeste.recorrer(operacion)

    def ponerElemento(self, elemMapa, unContenedor):
        unContenedor.noroeste = elemMapa

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.forma.noroeste

class Sureste(Orientacion):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'nombre'):
            super().__init__()
            self.nombre = "Sureste"

    def esSur(self):
        return True
    def caminar(self, unBicho):
        posicion = unBicho.posicion
        posicion.irSureste(unBicho)

    def recorrer(self, operacion, unContenedor, nivel=0, imprimir=False):
        if imprimir:
            print("   "*nivel, self, ": ", end=" ")
        unContenedor.forma.sureste.recorrer(operacion)

    def ponerElemento(self, elemMapa, unContenedor):
        unContenedor.sureste = elemMapa

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.forma.sureste

class Suroeste(Orientacion):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'nombre'):
            super().__init__()
            self.nombre = "Suroeste"

    def esSur(self):
        return True
    def caminar(self, unBicho):
        posicion = unBicho.posicion
        posicion.irSuroeste(unBicho)

    def recorrer(self, operacion, unContenedor, nivel=0, imprimir=False):
        if imprimir:
            print("   "*nivel, self, ": ", end=" ")
        unContenedor.forma.suroeste.recorrer(operacion)

    def ponerElemento(self, elemMapa, unContenedor):
        unContenedor.suroeste = elemMapa

    def obtenerElementoOREn(self, unContenedor):
        return unContenedor.forma.suroeste
