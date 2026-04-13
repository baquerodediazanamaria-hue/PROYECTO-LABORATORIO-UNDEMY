from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TipoHabitacion(Enum):
    """Tipos de habitación disponibles en el hotel."""
    SIMPLE = ("Simple", 1, 50.0)
    DOBLE = ("Doble", 2, 80.0)
    TRIPLE = ("Triple", 3, 110.0)
    SUITE = ("Suite", 4, 150.0)
    PRESIDENCIAL = ("Presidencial", 6, 300.0)
    
    def __init__(self, nombre: str, capacidad: int, precio_base: float):
        self.nombre_tipo = nombre
        self.capacidad_maxima = capacidad
        self.precio_base = precio_base

@dataclass
class Habitacion:
    """Representa una habitación del hotel con sus características."""
    
    numero: str
    tipo: TipoHabitacion
    precio_por_noche: float
    capacidad: int
    disponible: bool = True
    descripcion: str = ""
    caracteristicas: list = None
    
    def __post_init__(self):
        if self.caracteristicas is None:
            self.caracteristicas = []
        self._validar_datos()
    
    def _validar_datos(self):
        """Valida los datos de la habitación."""
        if not self.numero or not self.numero.strip():
            raise ValueError("El número de habitación no puede estar vacío")
        
        if self.precio_por_noche <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        
        if self.capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
    
    def marcar_ocupada(self):
        """Marca la habitación como ocupada."""
        self.disponible = False
    
    def marcar_disponible(self):
        """Marca la habitación como disponible."""
        self.disponible = True
    
    def calcular_costo(self, num_noches: int) -> float:
        """Calcula el costo total por un número de noches."""
        if num_noches <= 0:
            raise ValueError("El número de noches debe ser mayor a 0")
        return self.precio_por_noche * num_noches
    
    def to_dict(self) -> dict:
        """Convierte la habitación a diccionario para persistencia."""
        return {
            'numero': self.numero,
            'tipo': self.tipo.name,
            'precio_por_noche': self.precio_por_noche,
            'capacidad': self.capacidad,
            'disponible': self.disponible,
            'descripcion': self.descripcion,
            'caracteristicas': self.caracteristicas
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Habitacion':
        """Crea una habitación desde un diccionario."""
        return cls(
            numero=data['numero'],
            tipo=TipoHabitacion[data['tipo']],
            precio_por_noche=data['precio_por_noche'],
            capacidad=data['capacidad'],
            disponible=data.get('disponible', True),
            descripcion=data.get('descripcion', ''),
            caracteristicas=data.get('caracteristicas', [])
        )
    
    def __str__(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Habitación {self.numero} - {self.tipo.nombre_tipo} - ${self.precio_por_noche}/noche - {estado}"
