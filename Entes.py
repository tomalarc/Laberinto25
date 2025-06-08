from ElementoMapa import *
from Orientacion import *
from Modo import *
from Forma import *
from Juego import *
from Comando import *


class Ente():
    def __init__(self):
        self.nombre = "Ente"
        self.poder = 1
        self.posicion = None
        self.vidas = 5
        self.juego = None
        self.estadoEnte = Vivo()

    def atacar(self):
        self.estadoEnte.atacar(self)
    
    def avisar(self):
        pass
    def buscarTunel(self):
        pass
    def crearNuevoLaberinto(self, unTunel):
        pass
    def heMuerto(self):
        print(self.nombre, "ha muerto")
        self.vidas = 0
        self.estadoEnte = Muerto()
        self.avisar()

    def esAtacadoPor(self, algo):
        if self.estaVivo():
            print(self.nombre, "fue atacado por", algo.nombre, "--> ", end="")
            self.vidas = self.vidas - algo.poder
            
            if(self.vidas <= 0):
                self.heMuerto()
            else:
                print("Le quedan", self.vidas, "vidas\n")
        
    
    def estaVivo(self):
        return self.estadoEnte.estaVivo()
    
    def juegoClonaLaberinto(self):
        return self.juego.clonarLaberinto()
    def esPlayer(self):
        return False
    def puedeAtacar(self):
        pass

class Bicho(Ente):
    def __init__(self):
        super().__init__()
        self.nombre = "Bicho"
        self.modo = None
    
    def actua(self):
        if self.estadoEnte is not None:
            self.estadoEnte.actua(self)
    
    def avisar(self):
        self.juego.terminarBicho(self)
        self.juego.cambiarEstadoATerminar()
    def buscarTunel(self):
        self.modo.buscarTunelBicho(self)
    def esAgresivo(self):
        return self.modo.esAgresivo()
    def esPerezoso(self):
        return self.modo.esPerezoso()
    def estaHibernando(self):
        return self.modo.estaHibernando()
    
    def iniAgresivo(self):
        print(self.nombre, "cabmbia a modo Agresivo")
        self.modo = Agresivo()
        self.poder = 10
        self.vidas = 3
    def iniPerezoso(self):
        print(self.nombre, "cambia a modo Perezoso")
        self.modo = Perezoso()
        self.poder = 1
        self.vidas = 1
    def iniHibernando(self):
        print(self.nombre, "cambia a modo Hibernando")
        self.modo = Hibernacion()
        self.poder = 0
        self.vidas = 1
    
    def obtenerOrientacion(self):
        
        return self.posicion.obtenerOrientacion()
    def puedeActuar(self):
        self.modo.actua(self)
    def puedeAtacar(self):
        self.juego.buscarPersonaje(self)
    #SEGUN LA IMAGEN DE PHARO DEBERIA SER TRUE, PERO LO DEJO ASI POQUE NO ME CUADRA
    def esHabitacion(self):
        pass

class Player(Ente):
    def __init__(self, nombre="Personaje"):
        super().__init__()
        self.nombre = nombre
        self.vidas = 50
        self.poder = 10
        self.puntos = 0
        self.tesoro = None
        self.comandos = {}
    def __str__(self):
        return self.nombre
    def tieneElTesoro(self):
        if self.tesoro is not None:
            return True
        return False
    def avisar(self):
        self.juego.cambiarEstadoATerminar()
    def actua(self):
        self.estadoEnte.actua(self)
    def crearNuevoLaberinto(self, unTunel):
        unTunel.crearNuevoLaberinto(self)
    def irEste(self):
        self.posicion.irEste(self)
    def irOeste(self):
        self.posicion.irOeste(self)
    def irNorte(self):
        self.posicion.irNorte(self)
    def irSur(self):
        self.posicion.irSur(self)
    def revivir(self):
        self.vidas = 500
        self.estadoEnte = Vivo()
    def obtenerComandosExternos(self):
          # Agrega todos los comandos a la lista
        return self.posicion.obtenerComandos()
    def obtenerComandos(self):
        # Devuelve los comandos que el jugador puede ejecutar
        return self.comandos
    def obtenerComando(self, nombre):
        # Devuelve un comando por su nombre
        if nombre in self.comandos:
            return self.comandos[nombre]
        return None
    def agregarComando(self, comando):
        if comando not in self.comandos:
            self.comandos[comando.nombre] = comando
    def esPlayer(self):
        return True
    def puedeAtacar(self):
        self.juego.buscarBicho()

class EstadoEnte():
    def __init__(self):
        self.nombre = "EstadoEnte"
    def atacar(self, unEnte):
        pass
    def actua(self, unEnte):
        pass
    def estaVivo(self):
        pass

class Muerto(EstadoEnte):
    def __init__(self):
        super().__init__()
        self.nombre = "Muerto"
    def estaVivo(self):
        return False
    
class Vivo(EstadoEnte):
    def __init__(self):
        super().__init__()
        self.nombre = "Vivo"
    
    def atacar(self, unEnte):
        unEnte.puedeAtacar()
    
    def actua(self, unEnte):
        unEnte.puedeActuar()

    def estaVivo(self):
        return True