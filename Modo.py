
class Modo:
    def __init__(self):
        pass

    def actua(self, unBicho):
        self.caminar(unBicho)
        self.atacar(unBicho)


    #Quité dormir() ya que a la hora de jugar con la GUI, el metodo sleep() ralentiza el movimiento, no era comodo para jugar
    def atacar(self, unBicho):
        pass
        
    def caminar(self, unBicho):  
        pass
        



    def buscarTunelBicho(self, unBicho):
        pass
    def esAgresivo(self):
        return False
    
    def esPerezoso(self):
        return False
    
    def estaHibernando(self):
        return False

class Agresivo(Modo):
    def __init__(self):
        super().__init__()

    def esAgresivo(self):
        return True
    

    def atacar(self, unBicho):
        unBicho.atacar()
    def caminar(self, unBicho):
        ori = unBicho.obtenerOrientacion()
        ori.caminar(unBicho)
    
        
    def buscarTunelBicho(self, unBicho):
        contBicho = unBicho.posicion
        tunel = None
        for hijo in contBicho.hijos:
            if hijo.esTunel():
                tunel = hijo
                break
        if tunel is not None:
            tunel.entrar(unBicho)

class Perezoso(Modo):
    def __init__(self):
        super().__init__()

    def esPerezoso(self):
        return True
    def atacar(self, unBicho):
        unBicho.atacar()
    def caminar(self, unBicho):
        ori = unBicho.obtenerOrientacion()
        ori.caminar(unBicho)
    
    
    
class Hibernacion(Modo):
    def __init__(self):
        super().__init__()
    
    def estaHibernando(self):
        return True
