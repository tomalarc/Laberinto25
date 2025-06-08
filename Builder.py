from ElementoMapa import *
from Orientacion import *
from Modo import *
from Forma import *
from Juego import *
from Comando import *
from Creators import *
from Entes import *
from Comando import *
import json

class Director():
    def __init__(self):
        self.builder = None
        self.dict = {}
        self.cuadrado = True
    
    def procesar(self, direccion):
        self.leerArchivo(direccion)
        self.iniBuilder()
        self.fabricarLaberinto()
        self.fabricarJuego()
        self.fabricarBichos()
        print("\n")


    def leerArchivo(self, direccion):
        with open(direccion, "r") as file:
            try:
                self.dict = json.load(file)
                print("Archivo leido correctamente")

            except Exception as error:
                print(f"Error inesperado del tipo: {error}")


    def iniBuilder(self):
        if (self.dict["forma"] == "cuadrado"):
            self.builder = LaberintoBuilder()
            self.cuadrado = True
        elif (self.dict["forma"] == "rombo"):
            self.builder = LaberintoBuilderRombo()
            self.cuadrado = False
        else:
            raise Exception("Forma no soportada")
        

    def fabricarJuego(self):
        self.builder.fabricarJuego()
        self.builder.juego.laberintoCuadrado = self.cuadrado


    def fabricarLaberinto(self):
        self.builder.fabricarLaberinto()
        partesLaberinto = self.dict["laberinto"]
        for parte in partesLaberinto:
            self.fabricarLaberintoRecursivo(parte, self.builder.laberinto)

        puertas = self.dict["puertas"]

        for puerta in puertas:
            self.builder.fabricarPuerta(puerta[0], puerta[1], puerta[2], puerta[3])


    def fabricarBichos(self):

        bichos = self.dict.get("bichos", [])

        if(bichos != []):
            for bicho in bichos:
                self.builder.fabricarBichoModo(bicho["modo"], bicho["posicion"])

    def fabricarLaberintoRecursivo(self, dict, padre):
        cont = None
        if(dict["tipo"] == "habitacion"):
            cont = self.builder.fabricarHabitacion(dict["num"])
            comando = AbrirPuertas(cont)
            cont.agregarComando(comando)
        elif(dict["tipo"]== "armario"):
            cont = self.builder.fabricarArmarioEn(dict["num"], padre)
            comando = Entrar(cont)
            cont.agregarComando(comando)
        elif(dict["tipo"] == "bomba"):
            activa = dict["activa"]
            objeto = dict["objeto"]
            
            if objeto == "armario" and objeto is not None:
                arm = Armario()
                arm.numero = 0
                bomba = self.builder.fabricarBombaEn(padre, activa=activa, elemMapa=arm)
            else:
                bomba = self.builder.fabricarBombaEn(padre, activa=activa)
            
            comando = Entrar(bomba)
            bomba.agregarComando(comando)
        elif(dict["tipo"] == "vida"):
            objeto = dict["objeto"]
            if objeto == "armario" and objeto is not None:
                arm = Armario()
                arm.numero = 0
                vida = self.builder.fabricarVidaExtraEn(padre, elemMapa=arm)
            else:
                vida = self.builder.fabricarVidaExtraEn(padre)
            comando = Entrar(vida)
            vida.agregarComando(comando)
        elif(dict["tipo"] == "punto"):
            objeto = dict["objeto"]
            if objeto == "armario" and objeto is not None:
                arm = Armario()
                arm.numero = 0
                punto = self.builder.fabricarPuntoEn(padre, elemMapa=arm)
            else:
                punto = self.builder.fabricarPuntoEn(padre)
            comando = Entrar(punto)
            punto.agregarComando(comando)
        elif(dict["tipo"] == "tunel"):
            self.builder.fabricarTunelEn(padre)
        elif(dict["tipo"] == "tele"):
            hab = dict["hab"]
            tele = self.builder.fabricarTeletransporteEn(padre, num=hab)
            comando = Entrar(tele)
            tele.agregarComando(comando)
        elif(dict["tipo"] == "tesoro"):
            tesoro = self.builder.fabricarTesoroEn(padre)
            comando = Entrar(tesoro)
            tesoro.agregarComando(comando)
        if(dict["tipo"] == "habitacion" or dict["tipo"] == "armario"):
            print("Se intenta fabricar un elemento de tipo:", dict["tipo"])
            if (dict["hijos"] != [] and cont != None):
                for hijo in dict["hijos"]:
                    self.fabricarLaberintoRecursivo(hijo, cont)


class LaberintoBuilder():
    def __init__(self):
        self.laberinto = None
        self.juego = None
    
    def fabricarArmarioEn(self, numero, unContenedor):
        armario = Armario()
        armario.numero = numero
        armario.forma = self.fabricarFormaCuadrada()
        for ori in armario.obtenerOrientaciones():
            armario.ponerEnOrientacion(ori, self.fabricarPared())
        unContenedor.agregarHijo(armario)
        print(f"Se ha fabricado un Armario num:{armario.numero}")
        return armario
    def fabricarTeletransporteEn(self, unContenedor, num = None):
        
        tele = Teletransporte(num=num)
        unContenedor.agregarHijo(tele)
        return tele
    def fabricarTesoroEn(self, unContenedor):
        tesoro = Tesoro()
        unContenedor.agregarHijo(tesoro)
        return tesoro
    def fabricarBombaEn(self, unContenedor, elemMapa = None, activa = False):
        bomba = Bomba(elemMapa=elemMapa, activa=activa)
        unContenedor.agregarHijo(bomba)
        return bomba

    def fabricarVidaExtraEn(self, unContenedor, elemMapa = None):
        vida = VidaExtra(elemMapa=elemMapa)
        unContenedor.agregarHijo(vida)
        return vida
    def fabricarPuntoEn(self, unContenedor, elemMapa = None):
        punto = Punto(elemMapa=elemMapa)
        unContenedor.agregarHijo(punto)
        return punto
    def fabricarPared(self):
        return Pared()
    
    def fabricarHabitacion(self, num):
        hab = Habitación()
        hab.num = num
        hab.forma = self.fabricarFormaCuadrada()

        for orientacion in hab.forma.orientaciones:
            pared = self.fabricarPared()
            hab.ponerEnOrientacion(orientacion, pared)

        self.laberinto.agregarHabitacion(hab)
        print(f"Habitacion {num} agregada al Laberinto")
        return self.laberinto.obtener_habitacion(num)
    

    def fabricarJuego(self):
        self.juego = Juego()
        self.juego.prototipo = self.laberinto
        self.juego.laberinto = self.juego.clonarLaberinto()


    def fabricarLaberinto(self):
        print("Se ha fabricado un Laberinto")
        self.laberinto = Laberinto()
    
    
    
    def fabricarPuerta(self, lado1, ori1, lado2, ori2):
        
        #Se obtienen las habitaiones por el numero que se pasa por parametro
        hab1 = self.laberinto.obtener_habitacion(int(lado1))
        hab2 = self.laberinto.obtener_habitacion(int(lado2))

        #Se asigna cada habitacion a su lado correspondiente de la puerta
        puerta = Puerta(hab1, hab2)

        #Ya que solo se pasa la Ori por un string, este se convierte a un metodo para crear tal orientacion y asi asignarla como corresponde
        crearOri1= getattr(self, f"fabricar{ori1}")
        crearOri2 = getattr(self, f"fabricar{ori2}")
        hab1.ponerEnOrientacion(crearOri1(), puerta)
        hab2.ponerEnOrientacion(crearOri2(), puerta)
        print("Se ha fabricado una puerta:", puerta.nombre)
        return puerta
    
    
    
    def fabricarFormaCuadrada(self):
        forma=Cuadrado()
        forma.agregarOrientacion(self.fabricarNorte())
        forma.agregarOrientacion(self.fabricarSur())
        forma.agregarOrientacion(self.fabricarEste())
        forma.agregarOrientacion(self.fabricarOeste())
        return forma
    
    def fabricarBichoModo(self, strModo, posicion):
        hab = self.juego.laberinto.obtener_habitacion(int(posicion))
        metodo = getattr(self, f"fabricarBicho{strModo}")
        bicho = metodo(hab)
        hab.entrar(bicho)
        self.juego.agregarBicho(bicho)


    def fabricarBichoAgresivo(self, unaHab):
        bicho = Bicho()
        bicho.iniAgresivo()
        bicho.posicion = unaHab
        print("Se ha fabricado un Bicho Agresivo")
        return bicho
    
    def fabricarBichoPerezoso(self, unaHab):
        bicho = Bicho()
        bicho.iniPerezoso()
        bicho.posicion = unaHab
        print("Se ha fabricado un Bicho Perezodo")
        return bicho
    
    def fabricarTunelEn(self, unContenedor):
        tunel = Tunel()
        comando = Entrar(tunel)
        comando.receptor=tunel
        tunel.agregarComando(comando)
        unContenedor.agregarHijo(tunel)
        print("Se ha fabricado un Tunel")
        
    # Acá se aplica el Singleton
    def fabricarNorte(self):
        return Norte()
    
    def fabricarSur(self):
        return Sur()
    
    def fabricarEste(self):
        return Este()
    
    def fabricarOeste(self):
        return Oeste()



class LaberintoBuilderRombo(LaberintoBuilder):
    def __init__(self):
        super().__init__()
        
    def fabricarHabitacion(self, num):
            hab = Habitación()
            hab.num = num
            hab.forma = self.fabricarFormaDeRombo()

            for orientacion in hab.forma.orientaciones:
                pared = self.fabricarPared()
                hab.ponerEnOrientacion(orientacion, pared)

            self.laberinto.agregarHabitacion(hab)
            print(f"Habitacion {num} agregada al Laberinto con habitacioes Rombo")
            return self.laberinto.obtener_habitacion(num)
    
    def fabricarFormaDeRombo(self):
        forma=Rombo()
        forma.agregarOrientacion(self.fabricarNoreste())
        forma.agregarOrientacion(self.fabricarSureste())
        forma.agregarOrientacion(self.fabricarNoroeste())
        forma.agregarOrientacion(self.fabricarSuroeste())
        return forma
    

    def fabricarNoreste(self):
        return Noreste()
    
    def fabricarSureste(self):
        return Sureste()
    
    def fabricarNoroeste(self):
        return Noroeste()
    
    def fabricarSuroeste(self):
        return Suroeste()
    