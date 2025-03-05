from Orientacion import *

class ElementoMapa:
    def __init__(self, padre=None):
        self.padre = padre
        self.nombre = "ElementoMapa"

    def recorrer(self):
        pass

    def entrar(self, alguien=None):
        pass

    def esBomba(self):
        return False
    
    def esPared(self):
        return False
    
    def esPuerta(self):
        return False
    
    def esHabitacion(self):
        return False
    
    def esLaberinto(self):
        return False

class Contenedor(ElementoMapa):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.nombre = "Contenedor"
        self.hijos = []
        self.orientaciones = []

    def recorrer(self, nivel=0):
        indentacion = '  ' * nivel
        print(f"{indentacion}{self.nombre}")
        for orientacion in self.orientaciones:
            em = orientacion.obtenerElementoOREn(self)
            if em is not None:
                print(f"{indentacion}    {orientacion.nombre}: {em.nombre}")
        for hijo in self.hijos:
            if isinstance(hijo, Contenedor):
                hijo.recorrer(nivel + 1)
        

    def agregarHijo(self, em):
        em.padre = self
        self.hijos.append(em)

    def eliminarHijo(self, em):
        self.hijos.remove(em)

    def agregarOrientacion(self, orientacion):
        self.orientaciones.append(orientacion)
        
    def obtenerElementoOR(self, orientacion):
        return orientacion.obtenerElementoOR(self)

    def ponerEnOr(self, orientacion, em):
        orientacion.ponerElemento(em, self)

class Pared(ElementoMapa):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.nombre= "Pared"

    def entrar(self, alguien=None):

        if alguien is not None:
            print(alguien, "Ha chocado con una pared!")
        else:   
            print("Te has chocado con una pared!")

    def esPared(self):
        return True
    
class Puerta(ElementoMapa):
    def __init__(self, lado1, lado2, padre=None):
        super().__init__(padre)
        self.nombre = f"Puerta({lado1.nombre}, {lado2.nombre})"
        self.abierta = False
        self.lado1 = lado1
        self.lado2 = lado2

    def entrar(self, alguien):
        if self.abierta:
            print("La puerta está abierta")
        else:
            print("La puerta está cerrada")

    def abrir(self):
        self.abierta = True

    def cerrar(self):
        self.abierta = False

    def esPuerta(self):
        return True

class Hoja(ElementoMapa):
    def __init__(self, padre=None):
        super().__init__(padre)

class Decorator(Hoja):
    def __init__(self, em):
        super().__init__(em.padre)
        self.em = em

class Bomba(Decorator):
    def __init__(self, em):
        super().__init__(em)
        self.activa = False
    
    def entrar(self, alguien=None):
        if self.activa:
            print("¡Te has chocado con una bomba!")
        else:
            self.em.entrar(alguien)

    def esBomba(self):
        return True
    
class ParedBomba(Pared):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.activa = False

    def entrar(self, alguien=None):
        print("Te has chocado con una Pared Bomba")
    
class Habitación(Contenedor):
    def __init__(self, num, norte=None, sur=None, este=None, oeste=None, padre=None):
        super().__init__(padre)
        self.num = num
        self.norte = norte
        self.sur = sur
        self.este = este
        self.oeste = oeste
        self.nombre = "Habitación " + str(self.num)
        
    def entrar(self, alguien=None):
        print(f"Has entrado en la habitacion Nº{self.num}")

    def esHabitacion(self):
        return True

class Laberinto(Contenedor):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.nombre="Laberinto"

    def agregar_habitacion(self, unaHabitacion):
        self.hijos.append(unaHabitacion)
        unaHabitacion.padre = self

    def vaciarLaberinto(self):
        self.hijos.clear()
    
    def eliminar_habitacion(self, unaHabitacion):
        self.hijos.remove(unaHabitacion)

    def obtener_habitacion(self, num):
        for hijo in self.hijos:
            if hijo.num == num:
                return hijo
        return None

    def entrar(self, alguien=None):
        print("Estás en un laberinto")

    def esLaberinto(self):
        return True