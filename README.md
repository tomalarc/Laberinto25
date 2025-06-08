# REPOSITORIO PROYECTO DE LABERINTO - DISEÑO DE SOFTWARE - UCLM
Ultimo avance del proyecto

## Últimos Cambios y consideraciones

1. Se crearon 12 modificaciones extra al proyecto desarrollado en clases:
   a. Extension de algunos comandos:
     i. AbrirPuertas()
     ii. CerrarPuertas()
     iii. Atacar()
     iv. Arriba()
     v. Izquierda()
     vi. Derecha()
     vii. Abajo()
   b. Nuevo ConcreteStrategy en Modo de Bicho
   c. Nuevos Decorator:
     i. Puntos
     ii. VidaExtra
   d. Nuevos ElementoMapa:
     i. Tesoro
     ii. Teletransportador

3. Se implementó una pequeña libreria llamada graficos.py que utiliza pygame como base, con el fin de poder dibujar el laberinto
4. Verificar bien la ruta en la que se carga el json para evitar errores
