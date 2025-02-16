from abc import ABC, abstractmethod

# Producto abstracto
class Notification(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

# Productos concretos
class EmailNotification(Notification):
    def send(self, message: str):
        print(f"Enviando email: {message}")

class SMSNotification(Notification):
    def send(self, message: str):
        print(f"Enviando SMS: {message}")

# Factory Method
class NotificationFactory:
    @staticmethod
    def create_notification(type_: str) -> Notification:
        if type_ == "email":
            return EmailNotification()
        elif type_ == "sms":
            return SMSNotification()
        else:
            raise ValueError("Tipo de notificación no soportado")

# Uso
notificacion = NotificationFactory.create_notification("email")
notificacion.send("Hola desde Factory Method")

from functools import wraps

# Componente principal
class Mensaje:
    def enviar(self, contenido: str):
        print(f"Mensaje enviado: {contenido}")

# Decorador
def encriptado(metodo):
    @wraps(metodo)
    def wrapper(self, contenido: str):
        contenido_encriptado = contenido[::-1]  # Invirtiendo el texto como ejemplo
        print(f"Mensaje encriptado: {contenido_encriptado}")
        return metodo(self, contenido_encriptado)
    return wrapper

# Clase decorada
class MensajeSeguro(Mensaje):
    @encriptado
    def enviar(self, contenido: str):
        super().enviar(contenido)

# Uso
mensaje = MensajeSeguro()
mensaje.enviar("Hola Decorator")

from abc import ABC, abstractmethod

# Estrategia base
class EstrategiaPago(ABC):
    @abstractmethod
    def pagar(self, cantidad: float):
        pass

# Estrategias concretas
class PagoConTarjeta(EstrategiaPago):
    def pagar(self, cantidad: float):
        print(f"Pagando {cantidad} con tarjeta de crédito.")

class PagoConPayPal(EstrategiaPago):
    def pagar(self, cantidad: float):
        print(f"Pagando {cantidad} con PayPal.")

# Contexto
class CarritoDeCompras:
    def __init__(self, estrategia: EstrategiaPago):
        self.estrategia = estrategia

    def realizar_pago(self, cantidad: float):
        self.estrategia.pagar(cantidad)

# Uso
carrito = CarritoDeCompras(PagoConTarjeta())
carrito.realizar_pago(100)

carrito.estrategia = PagoConPayPal()  # Cambio de estrategia dinámico
carrito.realizar_pago(200)
