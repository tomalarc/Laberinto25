from Orientacion import *
from graficos import *
#Es todo objeto con el cual se puede interactuar en el mapa
class ElementoMapa:
    def __init__(self, padre=None):
        self.padre = padre
        self.comandos = []
        self.nombre = "ElementoMapa"

    def __str__(self):
        return self.nombre
    
    def dibujar(self, canvas, padre = None, num=None):
        pass

    def padre(self):
        return self.padre
    def setPadre(self, padre):
        self.padre = padre
    
    def agregarComando(self, comando):
        if comando not in self.comandos:
            self.comandos.append(comando)
        else:
            print("El comando ya existe en la lista de comandos de este elemento mapa")

    def obtenerComandos(self):
        return self.comandos
    
    def eliminarComando(self, comando):
        if comando in self.comandos:
            self.comandos.remove(comando)
        else:
            print("El comando no existe en la lista de comandos de este elemento mapa")
    
    def recorrer(self, operacion, nivel=0, imprimir=False):
        if imprimir:
            print("   "*nivel, end="")
        operacion(self)

    def entrar(self, alguien=None):
        pass
    def esElementoMapa(self):
        return True
    def esTunel(self):
        return False
    def esDecorator(self):
        return False
    def esArmario(self):
        return False
    def esUnTeletransporte(self):
        return False
    def esBomba(self):
        return False
    
    def esPared(self):
        return False
    def esTesoro(self):
        return False
    def esPuerta(self):
        return False
    
    def esHabitacion(self):
        return False
    
    def esLaberinto(self):
        return False

#Todo objeto ElementoMapa que contenga otros objetos, por lo que tiene una forma a su vez orientaciones. Cada contenedor ademas tiene un numero que lo identifica
class Contenedor(ElementoMapa):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.nombre = "Contenedor"
        self.hijos = []
        self.forma = None
        self.num = None

    def __str__(self):
        numero = self.num if self.num is not None else ""
        return self.nombre + str(numero)
    def obtenerComandos(self):
        comandos = self.comandos
        comandosNuevos = []
        for hijo in self.hijos:
            subcomandos = hijo.obtenerComandos()
            for sub in subcomandos:
                if sub not in comandos:
                    comandosNuevos.append(sub)
        total = comandos + comandosNuevos
        
        return total
    def recorrer(self, operacion, nivel=0, imprimir=False):

        if imprimir:
            # Aplicar la operación al nodo actual (con indentación)
            print("    " * nivel, end="")
            operacion(self)
            
            # Recorrer hijos (aumentando el nivel)
            print("    " * nivel + "-Hijos:")
            for hijo in self.hijos:
                
                hijo.recorrer(operacion, nivel= nivel + 1, imprimir=imprimir)  # ¡Llamada recursiva con level + 1!
            
            # Recorrer orientaciones (mismo nivel)
            print("    " * nivel + "-Orientaciones:")
            for orientacion in self.obtenerOrientaciones():
                orientacion.recorrer(operacion, self, nivel= nivel + 1, imprimir=imprimir)  # Mismo nivel +1
        else:
            operacion(self)
            for hijo in self.hijos:
                hijo.recorrer(operacion)
            for orientacion in self.obtenerOrientaciones():
                orientacion.recorrer(operacion, self, imprimir = imprimir)

    def agregarHijo(self, elemMapa):
        elemMapa.padre = self
        self.hijos.append(elemMapa)

    def entrar(self, alguien=None):
        if alguien is not None:
            print(alguien.nombre, "Ha entrado en el contenedor", self.nombre, (self.num if self.num is not None else ""))
            alguien.posicion = self
            alguien.buscarTunel()
    
    def eliminarHijo(self, hijo):
        if hijo in self.hijos:
            self.hijos.remove(hijo)
        else:
            print("El hijo no existe en la lista de hijos de este contenedor")

    def agregarOrientacion(self, orientacion):
        self.forma.agregarOrientacion(orientacion)
        
    def obtenerElementoOR(self, orientacion):
        return self.forma.obtenerElementoOR(orientacion)

    def obtenerOrientacion(self): 
        
        return self.forma.obtenerOrientacion()
    
    def obtenerOrientaciones(self):
        return self.forma.obtenerOrientaciones()

    def ponerEnOrientacion(self, orientacion, elemMapa):
        self.forma.ponerEnOrientacion(orientacion, elemMapa)

    def irEste(self, alguien):
        self.forma.irEste(alguien)

    def irOeste(self, alguien):
        self.forma.irOeste(alguien)
    
    def irNorte(self, alguien): 
        self.forma.irNorte(alguien)
    
    def irSur(self, alguien):
        self.forma.irSur(alguien)

    def irSureste(self, alguien):
        self.forma.irSureste(alguien)
    def irNoreste(self, alguien):
        self.forma.irNoreste(alguien)
    def irSuroeste(self, alguien):
        self.forma.irSuroeste(alguien)
    def irNoroeste(self, alguien):
        self.forma.irNoroeste(alguien)

class Armario(Contenedor):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.nombre = "Armario"
        self.numero=None
    def entrar(self, alguien):
        print(alguien, f"ha entrado en un armario que estaba dentro de {alguien.posicion}")
    def esArmario(self):
        return True

class Habitación(Contenedor):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.nombre = "Habitación"
    
    def dibujar(self, canvas, num=None):
        
        cuadrado1 = canvas.crear_cuadrado(
                    size=150,
                    color=(220, 220, 255),
                    has_walls=True,
                    wall_thickness=4
                )
        if (num+1) > 1:
            canvas.agregar_cuadrado(cuadrado1)
        else:
            canvas.agregar_cuadrado(cuadrado1, x=200, y=200)
        
        return cuadrado1
    def abrirPuertas(self):
        self.recorrer(lambda x: x.abrir() if x.esPuerta() else None)

    def cerrarPuertas(self):
        self.recorrer(lambda x: x.cerrar() if x.esPuerta() else None)

    def esHabitacion(self):
        return True

class Laberinto(Contenedor):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.nombre = "Laberinto"
    
    def dibujar(self, canvas, personaje=None, bichos=None):
        cuadrados = []

        #Se dibuja cada habitacion por separado
        for i, hijo in enumerate(self.hijos):
            dibujo = hijo.dibujar(canvas, i) #El dibujo de cada habitacion
            cuadrados.append([hijo, dibujo]) #Cada dibujo se guarda junto a su habitacion logica

        #La primera habitacion se dibuja en el centro del canvas, como referencia
        #Agrega un cuadrado hijo al centro de la habitacion
        
        #Se conecta cada habitacion con las otras a traves de las puertas
        for cuadrado in cuadrados:

            habitacion = cuadrado[0]
            dibujo = cuadrado[1]
            
            #Se verifica cada orientacion de cada habitacion
            for orientacion in habitacion.obtenerOrientaciones():
                
                elem = orientacion.obtenerElementoOREn(habitacion)
                
                #Si la orientacion es una puerta, se conecta con la habitacion contraria
                if elem.esPuerta():

                    # Se obtiene la habitacion contraria a la puerta
                    habContraria = elem.lado1 if elem.lado1 != habitacion else elem.lado2
                    
                    # Se busca el dibujo de la habitacion contraria en la lista de cuadrados
                    for cuadrado2 in cuadrados:
                        if cuadrado2[0] == habContraria:
                            dibujoAlt = cuadrado2[1]
                            break
                    
                    if elem.estaAbierta():
                        color = (255, 200, 200)
                    else:
                        color = (0, 0, 0)
                    # Conectar el dibujo de la habitacion actual con el dibujo de la habitacion contraria
                    if orientacion.esNorte():
                        dibujo.add_child_to_wall(Orientation.NORTE, 30, child_color=color)
                        dibujo.conectar(dibujoAlt, Orientation.NORTE)
                    elif orientacion.esSur():
                        dibujo.add_child_to_wall(Orientation.SUR, 30, child_color=color)
                        dibujo.conectar(dibujoAlt, Orientation.SUR)
                    elif orientacion.esEste():
                        dibujo.add_child_to_wall(Orientation.ESTE, 30, child_color=color)
                        dibujo.conectar(dibujoAlt, Orientation.ESTE)
                    elif orientacion.esOeste():   
                        dibujo.add_child_to_wall(Orientation.OESTE, 30, child_color=color)                       
                        dibujo.conectar(dibujoAlt, Orientation.OESTE)

            for hijo in habitacion.hijos:
                color = (143, 0, 255)
                if hijo.esArmario():
                    dibujo.add_child_to_corner("norte_este", 30, child_color=color)
                elif hijo.esBomba():           
                    dibujo.add_child_to_corner("norte_oeste", 30, child_color=color)
                elif hijo.esTunel():        
                    dibujo.add_child_to_corner("sur_este", 30, child_color=color)
                else:
                    dibujo.add_child_to_corner("sur_oeste", 30, child_color=color)

                if hijo.esTesoro():
                    dibujo.add_child_to_corner("sur_oeste", 30, child_color=(255, 215, 0))

            for bicho in bichos:
                if bicho.posicion == habitacion and bicho.estaVivo():
                    # Agregar el bicho al dibujo de la habitacion
                    if bicho.esAgresivo():
                        dibujo.add_child(25, child_color=(255, 0, 0))
                    elif bicho.esPerezoso():
                        dibujo.add_child(25, child_color=(255, 112, 0))
                    else:
                        dibujo.add_child(25, child_color=(143, 255, 0))
            
            if personaje.posicion == habitacion and personaje.estaVivo():
                # Agregar el personaje al dibujo de la habitacion
                dibujo.add_child(15, child_color=(61, 60, 255))  # Color rojo para el personaje
            
                    
    def imprimirLaberinto(self):
        print("\nLABERINTO IMPRESO:\n")
        self.recorrer(lambda x : print(x), imprimir=True)
        print("\n")
    def abrirPuertas(self):
        print("Abriendo todas las puertas\n")
        self.recorrer(lambda x: x.abrir() if x.esPuerta() else None)

    def cerrarPuertas(self):
        print("Cerrando todas las puertas\n")
        self.recorrer(lambda x: x.cerrar() if x.esPuerta() else None)

    def recorrer(self, operacion, nivel=0, imprimir=False):

        if imprimir:
            # Aplicar la operación al nodo actual (con indentación)
            print("    " * nivel, end="")
            operacion(self)
            
            # Recorrer hijos (aumentando el nivel)
            print("    " * nivel + "-Hijos:")
            for hijo in self.hijos:
                hijo.recorrer(operacion, nivel + 1, imprimir=imprimir)
        else:
            operacion(self)
            for hijo in self.hijos:
                hijo.recorrer(operacion)

    def agregarHabitacion(self, unaHabitacion):
        self.agregarHijo(unaHabitacion)

    def vaciarLaberinto(self):
        print("Todos los elementos del laberinto han sido eliminados")
        self.hijos.clear()
    
    def eliminar_habitacion(self, unaHabitacion):
        if unaHabitacion in self.hijos:
            self.hijos.remove(unaHabitacion)
            print("La habitación", unaHabitacion.num, "ha sido eliminada del laberinto")

    def obtener_habitacion(self, num):
        for hijo in self.hijos:
            if hijo.num == num:
                return hijo
        print("No se encontró la habitación con el número", num)
        return None

    def entrar(self, alguien=None):
        hab = self.obtener_habitacion(1)
        if(hab is not None):
            print(alguien.nombre, "está entrando en un laberinto por la habitacion 1")
            hab.entrar(alguien)

    def esLaberinto(self):
        return True

class Hoja(ElementoMapa):
    def __init__(self, padre=None):
        super().__init__()


class Tunel(Hoja):
    
    def __init__(self, padre=None):
        super().__init__(padre)
        self.nombre = "Tunel"
        self.laberinto = None

    def __str__(self):
        return self.nombre

    def aceptar(self, unVisitor):
        unVisitor.visitarTunel(self)
    def crearNuevoLaberinto(self, alguien):
        print(alguien.nombre, "crea un nuevo Laberinto")
        self.laberinto = alguien.juego.clonarLaberinto()

    def entrar(self, alguien):
        
        if self.laberinto is None:
            alguien.crearNuevoLaberinto(self)
            
        else:
            print(alguien.nombre, "entra en un nuevo laberinto")
            self.laberinto.entrar(alguien)

    def esTunel(self):
        return True

class Decorator(Hoja):
    def __init__(self, elemMapa):
        super().__init__()
        self.elemMapa = elemMapa
    def esDecorator(self):
        return True

class Bomba(Decorator):
    def __init__(self, elemMapa=None, activa=False):
        super().__init__(elemMapa)
        self.nombre = "Bomba"
        self.activa = activa
        self.poder = 1000
    def __str__(self):
        return self.nombre
    def entrar(self, alguien):
        if self.elemMapa is not None:
            self.elemMapa.entrar(alguien)
        if self.activa:
            print(alguien, " ha detonado una bomba!")
            alguien.esAtacadoPor(self)
        elif not self.activa:
            print(alguien.nombre, "ha encontrado una bomba desactivada", "" if self.elemMapa is None else "en " + str(self.elemMapa))

    def esBomba(self):
        return True

class VidaExtra(Decorator):
    def __init__(self, elemMapa=None):
        super().__init__(elemMapa)
        self.vidasExtra = 100
        self.nombre = "Vida Extra"
    def __str__(self):
        return self.nombre

    def entrar(self, alguien):
        if self.elemMapa is not None:
            print(alguien.nombre, f"ha encontrado una vida extra en {self.elemMapa}!")
        else:
            print(alguien.nombre, "ha encontrado una vida extra!")
        alguien.vidas += self.vidasExtra
        print("Ahora tiene", alguien.vidas, "vidas")
        if self.elemMapa is not None:
            self.elemMapa.entrar(alguien)

    def esVidaExtra(self):
        return True

class Punto(Decorator):
    def __init__(self, elemMapa=None):
        super().__init__(elemMapa)
        self.nombre = "Punto"
        self.puntos = 100

    def __str__(self):
        return self.nombre

    def entrar(self, alguien):
        if self.elemMapa is not None:
            print(alguien.nombre, f"ha encontrado un punto en {self.elemMapa}!")
        else:
            print(alguien.nombre, "ha encontrado un punto!")
        alguien.puntos += self.puntos
        print("Ahora tiene", alguien.puntos, "puntos")
        if self.elemMapa is not None:
            self.elemMapa.entrar(alguien)

class Pared(ElementoMapa):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.nombre= "Pared"

    def entrar(self, alguien=None):

        if alguien is not None:
            print(alguien.nombre, "Ha chocado con una pared!")
        else:   
            print("Te has chocado con una pared!")

    def esPared(self):
        return True
    
class ParedBomba(Pared):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.activa = False

    def entrar(self, alguien=None):
        print("Te has chocado con una Pared Bomba")
        
class Puerta(ElementoMapa):
    def __init__(self, lado1, lado2, padre=None):
        super().__init__(padre)
        self.estado = Cerrada()
        self.lado1 = lado1
        self.lado2 = lado2
        self.nombre = f"Puerta({lado1.nombre} {lado1.num}, {lado2.nombre} {lado2.num}) {self.estado.nombre}"

    def __str__(self):
        return f"Puerta({self.lado1.nombre} {self.lado1.num}, {self.lado2.nombre} {self.lado2.num}) {self.estado.nombre}"
    
    def entrar(self, alguien):
        self.estado.entrar(alguien, self)
        
    def abrir(self):
        self.estado.abrir(self)
       
    def cerrar(self):
        self.estado.cerrar(self)

    def esPuerta(self):
        return True
    
    def estaAbierta(self):
        return self.estado.estaAbierta()
    
    def puedeEntrar(self, alguien):
        if(alguien.posicion == self.lado1):
            self.lado2.entrar(alguien)
        else:
            self.lado1.entrar(alguien)

class Teletransporte(ElementoMapa):
    def __init__(self, padre=None, num=None):
        super().__init__(padre)
        self.nombre = "Teletransporte"
        self.num = num
        self.habitacion = None

    def __str__(self):
        return self.nombre
    def esUnTeletransporte(self):
        return True
    def entrar(self, alguien):
        if self.num is not None and alguien.esPlayer():
            self.habitacion = alguien.juego.laberinto.obtener_habitacion(self.num)
        if self.habitacion is None:
            print(alguien.nombre, "intenta teletransportarse pero no hay un habitacion definida")
        else:
            print(alguien.nombre, "se ha teletransportado a la habitación", self.habitacion.num)
            self.habitacion.entrar(alguien) 

class Tesoro(ElementoMapa):
    def __init__(self, padre=None):
        super().__init__(padre)
        self.nombre = "Tesoro"
        self.puntos = 1000000

    def __str__(self):
        return self.nombre
    def esTesoro(self):
        return True
    def entrar(self, alguien):
        print(alguien.nombre, "ha encontrado un tesoro!")
        if alguien.esPlayer() and alguien.estaVivo():
            print(f"¡Felicidades! {alguien.nombre} ha ganado el tesoro!")
            alguien.puntos += self.puntos
            alguien.tesoro = self
            alguien.juego.cambiarEstadoATerminar()

class EstadoPuerta:
    def __init__(self):
        self.nombre = "EstadoPuerta"
    
    def __str__(self):
        return self.nombre
    def abrir(self, puerta):
        pass
    def cerrar(self, puerta):
        pass
    def entrar(self, alguien, puerta):
        pass
    def estaAbierta(self):
        return False

class Abierta(EstadoPuerta):
    def __init__(self):
        super().__init__()
        self.nombre = "Abierta"

    def cerrar(self, puerta):
        print("Cerrando puerta")
        puerta.estado = Cerrada()
    
    def entrar(self, alguien, puerta):
        puerta.puedeEntrar(alguien)
    
    def estaAbierta(self):
        return True

class Cerrada(EstadoPuerta):
    def __init__(self):
        super().__init__()
        self.nombre = "Cerrada"

    def abrir(self, puerta):
        print("Abriendo puerta")
        puerta.estado = Abierta()
    
    def entrar(self, alguien, puerta):
        print(alguien.nombre, "Choca con la puerta cerrada")

