# REPOSITORIO PROYECTO DE LABERINTO - DISEÑO DE SOFTWARE - UCLM

**Último avance del proyecto**

## Últimos Cambios y Consideraciones

1. **Se crearon 12 modificaciones extra al proyecto desarrollado en clases:**

   **a. Extensión de algunos comandos:**
   - `AbrirPuertas()`
   - `CerrarPuertas()`
   - `Atacar()`
   - `Arriba()`
   - `Izquierda()`
   - `Derecha()`
   - `Abajo()`

   **b. Nuevo `ConcreteStrategy` en modo de Bicho**

   **c. Nuevos `Decorator`:**
   - `Puntos`
   - `VidaExtra`

   **d. Nuevos `ElementoMapa`:**
   - `Tesoro`
   - `Teletransportador`

2. **Se implementó una pequeña librería llamada `graficos.py` que utiliza `pygame` como base**, con el fin de poder dibujar el laberinto.

3. **Verificar bien la ruta en la que se carga el archivo JSON** para evitar errores.
