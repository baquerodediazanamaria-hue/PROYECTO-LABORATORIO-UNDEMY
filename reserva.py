from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional
from cliente import Cliente
from habitacion import Habitacion
from utils import obtener_fecha_actual

class EstadoReserva(Enum):
    """Estados posibles de una reserva."""
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    EN_CURSO = "En Curso"
    FINALIZADA = "Finalizada"
    CANCELADA = "Cancelada"

@dataclass
class Reserva:
    """Representa una reserva de habitación."""
    
    id: str
    cliente_id: str
    habitacion_numero: str
    fecha_checkin: date
    fecha_checkout: date
    numero_huespedes: int
    estado: EstadoReserva = EstadoReserva.PENDIENTE
    costo_total: float = 0.0
    fecha_creacion: str = field(default="")
    notas: str = ""
    
    def __post_init__(self):
        if isinstance(self.fecha_checkin, str):
            self.fecha_checkin = datetime.strptime(self.fecha_checkin, "%Y-%m-%d").date()
        if isinstance(self.fecha_checkout, str):
            self.fecha_checkout = datetime.strptime(self.fecha_checkout, "%Y-%m-%d").date()
        if isinstance(self.estado, str):
            self.estado = EstadoReserva[self.estado]
        
        self._validar_fechas()
    
    def _validar_fechas(self):
        """Valida que las fechas sean coherentes."""
        if self.fecha_checkin >= self.fecha_checkout:
            raise ValueError("La fecha de check-in debe ser anterior al check-out")
        
        if self.fecha_checkin < obtener_fecha_actual() and self.estado == EstadoReserva.PENDIENTE:
            raise ValueError("La fecha de check-in no puede ser anterior a hoy para nuevas reservas")
    
    def calcular_numero_noches(self) -> int:
        """Calcula el número de noches de la reserva."""
        delta = self.fecha_checkout - self.fecha_checkin
        return delta.days
    
    def calcular_costo(self, precio_por_noche: float) -> float:
        """Calcula el costo total de la reserva."""
        noches = self.calcular_numero_noches()
        self.costo_total = noches * precio_por_noche
        return self.costo_total
    
    def actualizar_estado(self, nuevo_estado: EstadoReserva):
        """Actualiza el estado de la reserva con validaciones."""
        transiciones_validas = {
            EstadoReserva.PENDIENTE: [EstadoReserva.CONFIRMADA, EstadoReserva.CANCELADA],
            EstadoReserva.CONFIRMADA: [EstadoReserva.EN_CURSO, EstadoReserva.CANCELADA],
            EstadoReserva.EN_CURSO: [EstadoReserva.FINALIZADA],
            EstadoReserva.FINALIZADA: [],
            EstadoReserva.CANCELADA: []
        }
        
        if nuevo_estado not in transiciones_validas.get(self.estado, []):
            raise ValueError(f"No se puede cambiar de {self.estado.value} a {nuevo_estado.value}")
        
        self.estado = nuevo_estado
    
    def puede_hacer_checkin(self) -> bool:
        """Verifica si se puede hacer check-in."""
        return (self.estado == EstadoReserva.CONFIRMADA and 
                self.fecha_checkin <= date.today())
    
    def puede_hacer_checkout(self) -> bool:
        """Verifica si se puede hacer check-out."""
        return self.estado == EstadoReserva.EN_CURSO
    
    def to_dict(self) -> dict:
        """Convierte la reserva a diccionario para persistencia."""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'habitacion_numero': self.habitacion_numero,
            'fecha_checkin': self.fecha_checkin.isoformat(),
            'fecha_checkout': self.fecha_checkout.isoformat(),
            'numero_huespedes': self.numero_huespedes,
            'estado': self.estado.name,
            'costo_total': self.costo_total,
            'fecha_creacion': self.fecha_creacion,
            'notas': self.notas
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reserva':
        """Crea una reserva desde un diccionario."""
        return cls(
            id=data['id'],
            cliente_id=data['cliente_id'],
            habitacion_numero=data['habitacion_numero'],
            fecha_checkin=data['fecha_checkin'],
            fecha_checkout=data['fecha_checkout'],
            numero_huespedes=data['numero_huespedes'],
            estado=data.get('estado', 'PENDIENTE'),
            costo_total=data.get('costo_total', 0.0),
            fecha_creacion=data.get('fecha_creacion', ''),
            notas=data.get('notas', '')
        )
    
    def __str__(self) -> str:
        return (f"Reserva {self.id} - Cliente: {self.cliente_id} - "
                f"Habitación: {self.habitacion_numero} - "
                f"{self.fecha_checkin} a {self.fecha_checkout} - "
                f"Estado: {self.estado.value}")
