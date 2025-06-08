class Comando():
    def __init__(self, receptor=None):

        self.receptor = receptor
    
    def ejecutar(self, alguien=None):
        pass

class AbrirPuerta(Comando):
    def __init__(self):
        super().__init__()
    def __str__(self):
        return "Comando Abrir"

    def ejecutar(self):
        self.receptor.abrir()

class CerrarPuertas(Comando):
    def __init__(self, receptor):
        super().__init__(receptor)
    def __str__(self):
        return "Comando Cerrar Todas las Puertas"
    
    def ejecutar(self, alguien=None):
        self.receptor.cerrarPuertas()
        self.receptor.comandos.remove(self)
        self.receptor.agregarComando(AbrirPuertas(self.receptor))
class AbrirPuertas(Comando):
    def __init__(self, receptor):
        super().__init__(receptor)
    def __str__(self):
        return "Comando Abrir Todas las Puertas"
    
    def ejecutar(self, alguien=None):
        self.receptor.abrirPuertas()
        self.receptor.comandos.remove(self)
        self.receptor.agregarComando(CerrarPuertas(self.receptor))


class Entrar(Comando):
    def __init__(self, receptor):
        super().__init__(receptor=receptor)
    def __str__(self):
        return "Comando Entrar"
    
    def ejecutar(self, alguien):
        self.receptor.entrar(alguien)

        if not self.receptor.esUnTeletransporte():
            self.receptor.eliminarComando(self)

class Arriba(Comando):
    def __init__(self, receptor):
        super().__init__(receptor=receptor)
        self.nombre = "Arriba"
    def __str__(self):
        return "Arriba"
    
    def ejecutar(self, alguien=None):
        if self.receptor is not None and self.receptor.esPlayer() and self.receptor.estaVivo():
            self.receptor.irNorte()
class Abajo(Comando):
    def __init__(self, receptor):
        super().__init__(receptor=receptor)
        self.nombre = "Abajo"
    def __str__(self):
        return "Abajo"
    
    def ejecutar(self, alguien=None):
        if self.receptor is not None and self.receptor.esPlayer() and self.receptor.estaVivo():
            self.receptor.irSur()
class Derecha(Comando):
    def __init__(self, receptor):
        super().__init__(receptor=receptor)
        self.nombre = "Derecha"
    def __str__(self):
        return "Derecha"
    
    def ejecutar(self, alguien=None):
        if self.receptor is not None and self.receptor.esPlayer() and self.receptor.estaVivo():
            self.receptor.irEste()
class Izquierda(Comando):
    def __init__(self, receptor):
        super().__init__(receptor=receptor)
        self.nombre = "Izquierda"
    def __str__(self):
        return "Izquierda"
    
    def ejecutar(self, alguien=None):
        if self.receptor is not None and self.receptor.esPlayer() and self.receptor.estaVivo():
            self.receptor.irOeste()

class Atacar(Comando):
    def __init__(self, receptor):
        super().__init__(receptor=receptor)
        self.nombre = "Atacar"
    def __str__(self):
        return "Atacar"
    
    def ejecutar(self, alguien=None):
        if self.receptor is not None and self.receptor.estaVivo():
            self.receptor.atacar()
