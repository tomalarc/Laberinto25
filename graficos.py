import pygame
import sys
from enum import Enum

class Orientation(Enum):
    """Enumeración para las orientaciones posibles de los cuadrados"""
    NORTE = 'norte'
    SUR = 'sur'
    ESTE = 'este'
    OESTE = 'oeste'
    CENTRO = 'centro'

class Square:
    def __init__(self, size, color=(255, 255, 255), has_walls=True, 
                 wall_color=(0, 0, 0), wall_thickness=3,
                 individual_walls=None, orientation=Orientation.CENTRO):
        """
        Crea un cuadrado con orientación y paredes personalizables.
        
        Args:
            size: Tamaño del cuadrado
            color: Color de relleno
            has_walls: Si tiene paredes visibles
            wall_color: Color general para todas las paredes
            wall_thickness: Grosor general para todas las paredes
            individual_walls: Configuraciones individuales para paredes
            orientation: Orientación del cuadrado
        """
        self.x = 0  # Se establecerá al posicionar
        self.y = 0  # Se establecerá al posicionar
        self.size = size
        self.color = color
        self.has_walls = has_walls
        self.wall_color = wall_color
        self.wall_thickness = wall_thickness
        self.children = []
        self.individual_walls = individual_walls if individual_walls else {}
        self.orientation = orientation
        self.connected_squares = {
            Orientation.NORTE: None,
            Orientation.SUR: None,
            Orientation.ESTE: None,
            Orientation.OESTE: None
        }
    
    def set_position(self, x, y):
        """Establece la posición del cuadrado"""
        self.x = x
        self.y = y
    
    def add_child(self, child_size, child_color=(200, 200, 200)):
        """Agrega un cuadrado hijo al centro."""
        child_x = self.x + (self.size - child_size) // 2
        child_y = self.y + (self.size - child_size) // 2
        child = Square(child_size, child_color, has_walls=False)
        child.set_position(child_x, child_y)
        self.children.append(child)
        return child
    def add_child_to_corner(self, corner, child_size, child_color=(200, 200, 200)):
        """
        Agrega un cuadrado hijo en una de las esquinas del cuadrado padre.
        
        Args:
            corner: Esquina donde colocar el hijo ('norte_este', 'norte_oeste', 'sur_este', 'sur_oeste')
            child_size: Tamaño del cuadrado hijo
            child_color: Color del cuadrado hijo
        
        Returns:
            El cuadrado hijo creado
        """
        # Calcular grosor de pared para ajuste de posición
        north_thickness = self.individual_walls.get(Orientation.NORTE, {}).get('thickness', self.wall_thickness)
        south_thickness = self.individual_walls.get(Orientation.SUR, {}).get('thickness', self.wall_thickness)
        east_thickness = self.individual_walls.get(Orientation.ESTE, {}).get('thickness', self.wall_thickness)
        west_thickness = self.individual_walls.get(Orientation.OESTE, {}).get('thickness', self.wall_thickness)
        
        if corner == 'norte_este':
            child_x = self.x + self.size - child_size - east_thickness//2
            child_y = self.y - child_size//2 + north_thickness//2
        elif corner == 'norte_oeste':
            child_x = self.x - child_size//2 + west_thickness//2
            child_y = self.y - child_size//2 + north_thickness//2
        elif corner == 'sur_este':
            child_x = self.x + self.size - child_size - east_thickness//2
            child_y = self.y + self.size - child_size//2 - south_thickness//2
        elif corner == 'sur_oeste':
            child_x = self.x - child_size//2 + west_thickness//2
            child_y = self.y + self.size - child_size//2 - south_thickness//2
        else:
            raise ValueError("Esquina no válida. Usar: 'norte_este', 'norte_oeste', 'sur_este' o 'sur_oeste'")
        
        child = Square(child_size, child_color, has_walls=False)
        child.set_position(child_x, child_y)
        self.children.append(child)
        return child
    def add_child_to_wall(self, wall, child_size, child_color=(200, 200, 200)):
        """Agrega un cuadrado hijo en una pared específica."""
        wall_config = self.individual_walls.get(wall, {})
        thickness = wall_config.get('thickness', self.wall_thickness)
        
        if wall == Orientation.NORTE:
            child_x = self.x + (self.size - child_size) // 2
            child_y = self.y - child_size // 2 + thickness // 2
        elif wall == Orientation.SUR:
            child_x = self.x + (self.size - child_size) // 2
            child_y = self.y + self.size - child_size // 2 - thickness // 2
        elif wall == Orientation.OESTE:
            child_x = self.x - child_size // 2 + thickness // 2
            child_y = self.y + (self.size - child_size) // 2
        elif wall == Orientation.ESTE:
            child_x = self.x + self.size - child_size // 2 - thickness // 2
            child_y = self.y + (self.size - child_size) // 2
        else:
            raise ValueError("Orientación no válida para pared")
            
        child = Square(child_size, child_color, has_walls=False)
        child.set_position(child_x, child_y)
        self.children.append(child)
        return child
    
    def conectar(self, otro_cuadrado, direccion, espacio=10):
        """
        Conecta este cuadrado con otro en la dirección especificada.
        
        Args:
            otro_cuadrado: Cuadrado a conectar
            direccion: Orientation (NORTE, SUR, ESTE, OESTE)
            espacio: Distancia entre los cuadrados
        """
        if direccion not in self.connected_squares:
            raise ValueError("Dirección no válida")
        
        self.connected_squares[direccion] = otro_cuadrado
        otro_cuadrado.connected_squares[self._direccion_opuesta(direccion)] = self
        
        # Calcular posición relativa
        if direccion == Orientation.NORTE:
            otro_cuadrado.set_position(
                self.x + (self.size - otro_cuadrado.size) // 2,
                self.y - otro_cuadrado.size - espacio
            )
        elif direccion == Orientation.SUR:
            otro_cuadrado.set_position(
                self.x + (self.size - otro_cuadrado.size) // 2,
                self.y + self.size + espacio
            )
        elif direccion == Orientation.OESTE:
            otro_cuadrado.set_position(
                self.x - otro_cuadrado.size - espacio,
                self.y + (self.size - otro_cuadrado.size) // 2
            )
        elif direccion == Orientation.ESTE:
            otro_cuadrado.set_position(
                self.x + self.size + espacio,
                self.y + (self.size - otro_cuadrado.size) // 2
            )
    
    def _direccion_opuesta(self, direccion):
        """Devuelve la dirección opuesta"""
        if direccion == Orientation.NORTE:
            return Orientation.SUR
        elif direccion == Orientation.SUR:
            return Orientation.NORTE
        elif direccion == Orientation.ESTE:
            return Orientation.OESTE
        elif direccion == Orientation.OESTE:
            return Orientation.ESTE
    
    def set_wall_style(self, wall, color=None, thickness=None):
        """Establece el estilo de una pared específica."""
        if wall not in [Orientation.NORTE, Orientation.SUR, Orientation.ESTE, Orientation.OESTE]:
            raise ValueError("Pared no válida")
            
        if wall not in self.individual_walls:
            self.individual_walls[wall] = {}
            
        if color is not None:
            self.individual_walls[wall]['color'] = color
        if thickness is not None:
            self.individual_walls[wall]['thickness'] = thickness
    
    def draw(self, surface):
        """Dibuja el cuadrado y sus hijos."""
        # Dibuja el cuadrado principal
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        
        if self.has_walls:
            # Dibuja cada pared con su configuración individual
            for wall in [Orientation.NORTE, Orientation.SUR, Orientation.ESTE, Orientation.OESTE]:
                wall_config = self.individual_walls.get(wall, {})
                color = wall_config.get('color', self.wall_color)
                thickness = wall_config.get('thickness', self.wall_thickness)
                
                if wall == Orientation.NORTE:
                    pygame.draw.rect(surface, color, (self.x, self.y, self.size, thickness))
                elif wall == Orientation.SUR:
                    pygame.draw.rect(surface, color, 
                                   (self.x, self.y + self.size - thickness, 
                                    self.size, thickness))
                elif wall == Orientation.ESTE:
                    pygame.draw.rect(surface, color, 
                                   (self.x + self.size - thickness, self.y, 
                                    thickness, self.size))
                elif wall == Orientation.OESTE:
                    pygame.draw.rect(surface, color, (self.x, self.y, thickness, self.size))
        
        # Dibuja los hijos
        for child in self.children:
            child.draw(surface)


class SquareCanvas:
    def __init__(self, width=1024, height=768, bg_color=(240, 240, 240)):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.bg_color = bg_color
        self.squares = []
        self.key_handlers = {}
        self.running = False
        self.clock = pygame.time.Clock()
        self.update_handlers = []
        self.font = pygame.font.SysFont('Arial', 20)  # Fuente por defecto
        self.texts = {}  # Diccionario para almacenar textos
    def remove_text(self, text_id):
        """Elimina un texto específico del canvas"""
        if text_id in self.text_elements:
            del self.text_elements[text_id]
    def clear_text(self):
        """Elimina todos los elementos de texto del canvas"""
        self.text_elements = {}  
    def add_text(self, name, text, position, color=(0, 0, 0)):
        """Añade o actualiza un texto en la pantalla"""
        self.texts[name] = {
            'content': text,
            'position': position,
            'color': color,
            'surface': self.font.render(text, True, color)
        }
    
    def draw_texts(self):
        """Dibuja todos los textos registrados"""
        for text_info in self.texts.values():
            self.screen.blit(text_info['surface'], text_info['position'])
    
    def run(self, fps=3):
        """Ejecuta el bucle principal con una tasa de refresco constante"""
        self.running = True
        while self.running:
            self.handle_events()
            
            # Ejecutar actualizaciones
            for handler in self.update_handlers:
                handler()
            
            # Dibujar elementos
            self.screen.fill(self.bg_color)
            for square in self.squares:
                square.draw(self.screen)
            self.draw_texts()
            
            pygame.display.flip()
            self.clock.tick(fps)
        
        pygame.quit()
        sys.exit()
    
    def add_update_handler(self, handler):
        """Añade una función que se ejecutará en cada frame"""
        self.update_handlers.append(handler)
    
    def handle_events(self):
        """Maneja todos los eventos de pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_handlers:
                    self.key_handlers[event.key]()
    
    def on_key_press(self, key):
        """Decorador para asignar funciones a teclas"""
        def decorator(func):
            self.key_handlers[key] = func
            return func
        return decorator
    
    def crear_cuadrado(self, size, **kwargs):
        """Crea un cuadrado sin posición inicial"""
        square = Square(size, **kwargs)
        return square
    
    def agregar_cuadrado(self, square, x=None, y=None):
        """Agrega un cuadrado al lienzo"""
        if x is not None and y is not None:
            square.set_position(x, y)
        self.squares.append(square)
        return square
    
    