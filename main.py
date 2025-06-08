from ElementoMapa import *
from Builder import *
#TOMÁS ALARCÓN SEGOVIA
#PROYECTO DE DISEÑO DE SOFTWARE, 2025

def main():

    # Configuración inicial del juego
    director = Director()
    director.procesar(r"C:\Users\Tomás\Desktop\Proyecto Laberinto\Tomás Alarcón_Proyecto Laberinto_2025\Mapas\pruebaCuadrado.json")
    juego = director.builder.juego
    
    #Prueba de algunos metodos utiles para la terminal
    juego.imprimirLaberinto()
    juego.ubicacionDeEntes()
    
    #Aca comienza el juego
    #PARA LA GUI, LAS TECLAS DE MOVIMIENTO, SON W,A,D Y S PARA MOVERSE, Y ESPACIO PARA ATACAR
    juego.jugar(personaje="Tomas", gui=True)


    #PROYECTOS DE TEST (DEBE EJECUTARSE CON LO QUE ESTÁ ARRIBA)
    #A CONTINUACION SE PRESENTAN ALGUNOS TEST ESPECIFICOS PARA LAS FUNCIONALIDADES EXTRA (EL RESTO SE PUEDE VER CON EL JSON)
    # (DESCOMENTAR PARA PODER PROBARLOS, Y TAMBIEN SE DEBE DESACTIVAR LA GUI)
    
    #1) OBTENER TESORO:
    #juego.obtenerHabitacion(7).entrar(juego.person)
    #juego.person.posicion.obtenerComandos()[1].ejecutar(juego.person)

    #2) TOMAR VIDAS:
    #juego.person.posicion.obtenerComandos()[1].ejecutar(juego.person)

    #3) TELETRANSPORTARSE:
    #juego.obtenerHabitacion(8).entrar(juego.person)
    #juego.person.posicion.obtenerComandos()[1].ejecutar(juego.person)
if __name__ == "__main__":
    main()