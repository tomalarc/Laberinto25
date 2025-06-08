from Creators import *
from ElementoMapa import *
from Orientacion import *
from Modo import *
from Forma import *
import threading
from time import sleep
import copy

from graficos import *

import pygame


class GameObserver:
    def __init__(self, juego):
        self.juego = juego
        self.canvas = SquareCanvas()
        self.setup_ui()
        self.setup_input_handling()
        self.setup_automatic_updates()
    
    def setup_ui(self):
        """Configuración inicial de la interfaz de usuario"""
        self.update_ui_texts()
    
    def update_ui_texts(self):
        """Actualiza todos los elementos de texto en la UI"""
        self.update_game_info()
        self.mostrar_comandos_disponibles()
    
    def update_game_info(self):
        """Muestra la información principal del juego"""
        personaje = getattr(self.juego, 'person', None)
        if not personaje:
            return

        # Calculamos posición (esquina superior derecha)
        pos_x = self.canvas.screen.get_width() - 350
        pos_y = 20
        
        # Vidas del personaje
        self.canvas.add_text(
            "vidas",
            f"Vidas: {getattr(personaje, 'vidas', 0)}",
            (pos_x, pos_y),
            (255, 0, 0)  # Rojo
        )
        
        # Contador de bichos
        bichos = getattr(self.juego, 'bichos', [])
        bichos_vivos = sum(1 for b in bichos if getattr(b, 'estaVivo', lambda: False)())
        self.canvas.add_text(
            "bichos",
            f"Bichos: {bichos_vivos}/{len(bichos)}",
            (pos_x, pos_y + 30),
            (0, 255, 0)  # Verde
        )
        
        # Habitación actual
        hab_actual = getattr(getattr(personaje, 'posicion', None), 'num', "?")
        self.canvas.add_text(
            "habitacion",
            f"Habitación: {hab_actual}",
            (pos_x, pos_y + 60),
            (0, 0, 255)  # Azul
        )
        # Puntos del personaje
        puntos = getattr(personaje, 'puntos', 0)
        self.canvas.add_text(
            "puntos",
            f"Puntos: {puntos}",
            (pos_x, pos_y + 90),
            (255, 165, 0)  # Naranja
        )
    
    def mostrar_comandos_disponibles(self):
        """Versión corregida que maneja adecuadamente las actualizaciones"""
        personaje = getattr(self.juego, 'person', None)
        if not personaje or not hasattr(personaje, 'obtenerComandos'):
            return

        try:
            # 1. Limpiar comandos anteriores del canvas
            for i in range(9):  # Eliminar todos los posibles textos de comandos
                self.canvas.texts.pop(f"comando_{i}", None)
            
            # 2. Obtener comandos actualizados
            comandos = personaje.obtenerComandosExternos() or []
            
            # 3. Configuración visual
            pos_x = self.canvas.screen.get_width() - 350
            pos_y = 170
            color = (0, 0, 0)
            
            # 4. Dibujar título (siempre visible)
            self.canvas.add_text(
                "comandos_titulo",
                "Comandos disponibles:",
                (pos_x, pos_y),
                color
            )
            
            # 5. Dibujar comandos actuales
            for i, cmd in enumerate(comandos[:9]):
                cmd_name = cmd.__class__.__name__.replace("Comando", "").strip()
                if cmd.receptor.esDecorator():
                    if cmd.receptor.elemMapa is not None:
                        cmd_name = f"{cmd_name} ({cmd.receptor.elemMapa.nombre})"
                    else:   
                        cmd_name = f"{cmd_name} ({cmd.receptor.nombre})"
                else:
                    cmd_name = f"{cmd_name} ({cmd.receptor.nombre})"
                self.canvas.add_text(
                    f"comando_{i}",

                    f"{i+1}. {cmd_name}",
                    (pos_x + 10, pos_y + 25 + i * 25),
                    color
                )
                
        except Exception as e:
            print(f"Error actualizando comandos: {e}")
        
    
    def formatear_nombre_comando(self, comando):
        """Formatea el nombre del comando para visualización"""
        if not comando:
            return "Acción"
        
        nombre = comando.__class__.__name__
        nombre = nombre.replace("Comando", "").replace("_", " ").strip()
        return nombre or "Acción"
    
    def setup_automatic_updates(self):
        """Configura las actualizaciones automáticas del juego"""
        self.canvas.add_update_handler(self.update_game_state)
    
    def update_game_state(self):
        """Actualiza el estado del juego en cada frame"""
        # Actualizar bichos
        for bicho in getattr(self.juego, 'bichos', []):
            if getattr(bicho, 'estaVivo', lambda: False)():
                bicho.actua()
        
        # Actualizar UI
        self.update_ui_texts()
        self.update(self.juego)
    
    def setup_input_handling(self):
        """Configura los controles de entrada"""
        # Movimiento básico (WASD)
        controles = {
            pygame.K_w: 'Arriba',
            pygame.K_s: 'Abajo',
            pygame.K_a: 'Izquierda',
            pygame.K_d: 'Derecha',
            pygame.K_SPACE: 'Atacar',
        }
        
        for tecla, clave_comando in controles.items():
            @self.canvas.on_key_press(tecla)
            def handler(clave=clave_comando):
                personaje = self.juego.person
                if personaje:
                    comando = personaje.obtenerComando(clave)
                    if comando:
                        comando.ejecutar(personaje)
                        # Actualización de la UI
                        self.update_ui_texts()
                        self.juego.notify_observers()
        
        # Ejecución de comandos con teclas numéricas (1-9)
        for num in range(1, 10):
            @self.canvas.on_key_press(getattr(pygame, f"K_{num}"))
            def ejecutar(indice=num-1):
                self.ejecutar_comando(indice)
    
    def ejecutar_comando(self, indice):
        """Versión optimizada con actualización garantizada"""
        try:
            personaje = self.juego.person
            if not personaje or not personaje.estaVivo():
                return
                
            comandos = personaje.obtenerComandosExternos()
            if 0 <= indice < len(comandos):
                # 1. Ejecutar comando (puede modificar la lista)
                comandos[indice].ejecutar(personaje)
                
                # 2. Actualización directa e inmediata
                self.mostrar_comandos_disponibles()
                pygame.display.flip()  # Forzar refresco
                
        except Exception as e:
            print(f"Error en comando: {e}")
        
    def update(self, juego):
        """Actualiza la visualización del laberinto"""
        self.canvas.squares = []  # Limpiar elementos anteriores
        
        if hasattr(juego, 'laberinto') and hasattr(juego.laberinto, 'dibujar'):
            juego.laberinto.dibujar(
                self.canvas,
                getattr(juego, 'person', None),
                getattr(juego, 'bichos', [])
            )
    
    def run(self):
        """Inicia el bucle principal del juego"""
        self.update(self.juego)
        self.canvas.run()

class Juego:

    def __init__(self):
        self.laberinto = None
        self.bichos = []
        self.hilos = {}
        self.person = None
        self.prototipo = None
        self.observers = []  # Lista de observadores
        self.estado = Iniciar()
        self.laberintoCuadrado = True




    # METODOS UTILES PARA EL JUEGO
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)
    
    def jugar(self, personaje, gui = True):

    
        if gui and self.juegoConLaberintoCuadrado():
            self.cambiarEstadoAIniciar(personaje)
            # Configurar el sistema gráfico
            observer = GameObserver(self)
            self.add_observer(observer)
            observer.run()
        elif gui and not self.juegoConLaberintoCuadrado():
            print("\nNo se puede ejecutar la GUI, ya que solo está adaptada para laberintos cuadrados\n")
        elif not gui:
            self.cambiarEstadoAIniciar(personaje)
    
    def juegoConLaberintoCuadrado(self):
        return self.laberintoCuadrado
    def abrirPuertas(self):
        self.laberinto.abrirPuertas()
        self.notify_observers()
    
    def cerrarPuertas(self):
        self.laberinto.cerrarPuertas()
        self.notify_observers()
    
    def agregarPersonaje(self, nombre):
        creator = Creator()
        self.person = creator.fabricarPersonaje(nombre)
        self.person.juego = self
        self.laberinto.entrar(self.person)

        arriba = Arriba(self.person)
        self.person.agregarComando(arriba)

        abajo = Abajo(self.person)
        self.person.agregarComando(abajo)

        izquierda = Izquierda(self.person)
        self.person.agregarComando(izquierda)

        derecha = Derecha(self.person)
        self.person.agregarComando(derecha)

        atacar = Atacar(self.person)
        self.person.agregarComando(atacar)

        
        self.notify_observers()

    def ubicacionDeEntes(self):
        print("\nUBICACION DE ENTES:")
        if self.bichos != []:
            for bicho in self.bichos:
                print(bicho.nombre, " -> ", bicho.posicion)
        if self.person is not None:
            print(self.person.nombre, " -> ", self.person.posicion)

    def imprimirLaberinto(self):
        self.laberinto.imprimirLaberinto()
    
    def crearLaberinto2Hab2Bichos(self):
        creator = Creator()
        self.laberinto = creator.fabricarLaberintoVacio()
        hab = creator.fabricarHabitacion(1)
        hab2 = creator.fabricarHabitacion(2)
        puerta = creator.fabricarPuerta(hab, hab2)
        hab.forma.ponerEnOrientacion(Este(), puerta)
        hab2.forma.ponerEnOrientacion(Oeste(), puerta)
        bicho1 = creator.fabricarBichoAgresivo(hab)
        bicho2 = creator.fabricarBichoPerezoso(hab2)
        self.bichos.append(bicho1)
        self.bichos.append(bicho2)
        self.laberinto.agregarHabitacion(hab)
        self.laberinto.agregarHabitacion(hab2)

    def agregarBicho(self, bicho):
        bicho.juego = self  
        self.bichos.append(bicho)
    
    def obtenerHabitacion(self, num):
        return self.laberinto.obtener_habitacion(num)





    #METODOS UTILES DURANTE EL JUEGO
    def buscarBicho(self):
        
        posPer = self.person.posicion
        
        for bicho in self.bichos:
            posBicho = bicho.posicion
            if posBicho == posPer and bicho.estaVivo():
                bicho.esAtacadoPor(self.person)
                if not bicho.estaVivo():
                    self.terminarBicho(bicho)
    
    def buscarPersonaje(self, bicho):

        if self.person is not None:
            posPer = self.person.posicion
            if posPer == bicho.posicion and self.person.estaVivo():
                self.person.esAtacadoPor(bicho)
                bicho.posicion = posPer
        else:
            print("No hay personaje en el juego")

    def clonarLaberinto(self):
        return copy.deepcopy(self.prototipo)
    
    def lanzarBichos(self):
        for bicho in self.bichos:
            self.lanzarBicho(bicho)
    
    def lanzarBicho(self, bicho):
        
        # Imprimir en consola
        print(f"{bicho.nombre} se lanza")
        
        # Definir la función que ejecutará el hilo
        def ejecutar_acciones():
            while bicho is not None:
                if bicho.estaVivo() and not bicho.estaHibernando():
                    bicho.actua()
                    sleep(0.5)
                else:
                    break
        
        # Crear y lanzar el hilo 
        proceso = threading.Thread(target=ejecutar_acciones)
        proceso.start()
        
        # Almacenar el hilo en un diccionario 
        self.hilos[bicho] = proceso
    





    #METODOS DE TERMINO DEL JUEGO
    
    def todosLosBichosMuertos(self):
        muertos = True
        for bicho in self.bichos:
            if bicho.estaVivo():
                muertos = False
        return muertos
    

    def terminarBicho(self, bicho):

        hilo = self.hilos.get(bicho, None)
        if hilo is not None and hilo.is_alive():
            if threading.current_thread() != hilo:
                hilo.join()
        

    def terminarBichos(self):
        for bicho in self.bichos:
            if bicho.estaVivo():
                bicho.heMuerto()
    
    def hibernarBichos(self):
        for bicho in self.bichos:
            if bicho.estaVivo():
                bicho.iniHibernando()
                self.terminarBicho(bicho)

    def pierdePersonaje(self):
        print("FIN DEL JUEGO: Ganan los bichos\n")
        self.hibernarBichos()
        
    
    def ganaPersonaje(self):
        print(f"FIN DEL JUEGO: Gana {self.person.nombre}\n")
        self.terminarBichos()

    def cambiarEstadoATerminar(self):
        self.estado = Terminar()
        self.estado.actualizar(self)
    
    def cambiarEstadoAIniciar(self, personaje):
        self.estado = Iniciar()
        self.estado.actualizar(personaje, self)
    
#ESTADOS DEL JUEGO

class EstadoJuego:
    def __init__(self):
        self.nombre = "Estado"
    def __str__(self):
        return self.nombre
    
    def actualizar(self):
        pass

    def estaIniciado(self):
        return False
    def estaJugando(self):
        return False
    def estaTerminado(self):
        return False

class Iniciar(EstadoJuego):
    def __init__(self):
        super().__init__()
        self.nombre = "Iniciar"
    def __str__(self):
        return "Inicio"
    def estaIniciado(self):
        return True
    def actualizar(self, personaje, juego):
        if juego.person is not None:
            nombre = juego.person.nombre
            juego.person = None
            juego.agregarPersonaje(nombre)
        elif juego.person is not None and not juego.person.esta():
            juego.person.revivir()
        else:
            juego.agregarPersonaje(personaje)
        for bicho in juego.bichos:
            if not bicho.estaVivo():
                if bicho.esAgresivo():
                    bicho.iniAgresivo()
                elif bicho.esPerezoso():
                    bicho.iniPerezoso()
        juego.lanzarBichos()
        juego.estado = Jugando()
        
class Jugando(EstadoJuego):
    def __init__(self):
        super().__init__()
        self.nombre = "Jugando"
    def __str__(self):
        return "Jugando"
    def estaJugando(self):
        return True
    
class Terminar(EstadoJuego):
    def __init__(self):
        super().__init__()
        self.nombre = "Terminar"
    def __str__(self):
        return "Termino"
    def actualizar(self, juego):
        
        if juego.person.estaVivo() and (juego.todosLosBichosMuertos() or juego.person.tieneElTesoro()):
            juego.ganaPersonaje()
        elif juego.person.estaVivo() and not juego.todosLosBichosMuertos():
            juego.estado = Jugando()
        elif not juego.person.estaVivo() and not juego.todosLosBichosMuertos():
            juego.pierdePersonaje()
            
        
        

    def estaTerminado(self):
        return True
    
    