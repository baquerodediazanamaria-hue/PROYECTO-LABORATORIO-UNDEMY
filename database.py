import json
import os
from typing import List, Optional, Dict
from datetime import datetime
from cliente import Cliente
from habitacion import Habitacion, TipoHabitacion
from reserva import Reserva

class Database:
    """Maneja la persistencia de datos en archivos JSON."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.hotel_data_file = os.path.join(data_dir, "hotel_data.json")
        self.clientes_data_file = os.path.join(data_dir, "clientes_data.json")
        
        self._crear_directorio()
        self._inicializar_archivos()
    
    def _crear_directorio(self):
        """Crea el directorio de datos si no existe."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _inicializar_archivos(self):
        """Inicializa los archivos JSON si no existen."""
        if not os.path.exists(self.hotel_data_file):
            datos_iniciales = {
                'habitaciones': self._generar_habitaciones_iniciales(),
                'reservas': [],
                'contadores': {
                    'cliente': 1,
                    'reserva': 1
                }
            }
            self._guardar_json(self.hotel_data_file, datos_iniciales)
        
        if not os.path.exists(self.clientes_data_file):
            self._guardar_json(self.clientes_data_file, {'clientes': []})
    
    def _generar_habitaciones_iniciales(self) -> List[dict]:
        """Genera las habitaciones iniciales del hotel."""
        habitaciones = [
            Habitacion("101", TipoHabitacion.SIMPLE, 50.0, 1, True, 
                      "Habitación simple con cama individual", ["WiFi", "TV", "Baño privado"]),
            Habitacion("102", TipoHabitacion.SIMPLE, 50.0, 1, True,
                      "Habitación simple con vista al jardín", ["WiFi", "TV", "Baño privado"]),
            Habitacion("201", TipoHabitacion.DOBLE, 80.0, 2, True,
                      "Habitación doble con cama matrimonial", ["WiFi", "TV", "Minibar", "Balcón"]),
            Habitacion("202", TipoHabitacion.DOBLE, 85.0, 2, True,
                      "Habitación doble con dos camas", ["WiFi", "TV", "Minibar", "Vista ciudad"]),
            Habitacion("203", TipoHabitacion.TRIPLE, 110.0, 3, True,
                      "Habitación triple familiar", ["WiFi", "TV", "Minibar", "Sofá cama"]),
            Habitacion("301", TipoHabitacion.SUITE, 150.0, 4, True,
                      "Suite con sala de estar y jacuzzi", ["WiFi", "TV", "Minibar", "Jacuzzi", "Sala"]),
            Habitacion("302", TipoHabitacion.SUITE, 160.0, 4, True,
                      "Suite Premium con vista panorámica", ["WiFi", "TV", "Minibar", "Terraza"]),
            Habitacion("401", TipoHabitacion.PRESIDENCIAL, 300.0, 6, True,
                      "Suite Presidencial con comedor privado", 
                      ["WiFi", "TV", "Minibar", "Jacuzzi", "Sala", "Comedor", "Terraza"])
        ]
        return [hab.to_dict() for hab in habitaciones]
    
    def _leer_json(self, filepath: str) -> dict:
        """Lee un archivo JSON."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al leer {filepath}: {e}")
    
    def _guardar_json(self, filepath: str, data: dict):
        """Guarda datos en un archivo JSON."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise IOError(f"Error al guardar {filepath}: {e}")
    
    def guardar_cliente(self, cliente: Cliente) -> bool:
        """Guarda un cliente en la base de datos."""
        try:
            data = self._leer_json(self.clientes_data_file)
            clientes = data.get('clientes', [])
            
            for i, c in enumerate(clientes):
                if c['documento'] == cliente.documento:
                    clientes[i] = cliente.to_dict()
                    data['clientes'] = clientes
                    self._guardar_json(self.clientes_data_file, data)
                    return True
            
            clientes.append(cliente.to_dict())
            data['clientes'] = clientes
            self._guardar_json(self.clientes_data_file, data)
            return True
        except Exception as e:
            print(f"Error al guardar cliente: {e}")
            return False
    
    def obtener_cliente(self, documento: str) -> Optional[Cliente]:
        """Obtiene un cliente por documento."""
        try:
            data = self._leer_json(self.clientes_data_file)
            clientes = data.get('clientes', [])
            
            for c in clientes:
                if c['documento'] == documento:
                    return Cliente.from_dict(c)
            return None
        except Exception as e:
            print(f"Error al obtener cliente: {e}")
            return None
    
    def obtener_todos_clientes(self) -> List[Cliente]:
        """Obtiene todos los clientes."""
        try:
            data = self._leer_json(self.clientes_data_file)
            clientes = data.get('clientes', [])
            return [Cliente.from_dict(c) for c in clientes]
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            return []
    
    def guardar_habitacion(self, habitacion: Habitacion) -> bool:
        """Actualiza el estado de una habitación."""
        try:
            data = self._leer_json(self.hotel_data_file)
            habitaciones = data.get('habitaciones', [])
            
            for i, h in enumerate(habitaciones):
                if h['numero'] == habitacion.numero:
                    habitaciones[i] = habitacion.to_dict()
                    data['habitaciones'] = habitaciones
                    self._guardar_json(self.hotel_data_file, data)
                    return True
            return False
        except Exception as e:
            print(f"Error al guardar habitación: {e}")
            return False
    
    def obtener_habitacion(self, numero: str) -> Optional[Habitacion]:
        """Obtiene una habitación por número."""
        try:
            data = self._leer_json(self.hotel_data_file)
            habitaciones = data.get('habitaciones', [])
            
            for h in habitaciones:
                if h['numero'] == numero:
                    return Habitacion.from_dict(h)
            return None
        except Exception as e:
            print(f"Error al obtener habitación: {e}")
            return None
    
    def obtener_todas_habitaciones(self) -> List[Habitacion]:
        """Obtiene todas las habitaciones."""
        try:
            data = self._leer_json(self.hotel_data_file)
            habitaciones = data.get('habitaciones', [])
            return [Habitacion.from_dict(h) for h in habitaciones]
        except Exception as e:
            print(f"Error al obtener habitaciones: {e}")
            return []
    
    def guardar_reserva(self, reserva: Reserva) -> bool:
        """Guarda una reserva en la base de datos."""
        try:
            data = self._leer_json(self.hotel_data_file)
            reservas = data.get('reservas', [])
            
            for i, r in enumerate(reservas):
                if r['id'] == reserva.id:
                    reservas[i] = reserva.to_dict()
                    data['reservas'] = reservas
                    self._guardar_json(self.hotel_data_file, data)
                    return True
            
            reservas.append(reserva.to_dict())
            data['reservas'] = reservas
            self._guardar_json(self.hotel_data_file, data)
            return True
        except Exception as e:
            print(f"Error al guardar reserva: {e}")
            return False
    
    def obtener_reserva(self, id_reserva: str) -> Optional[Reserva]:
        """Obtiene una reserva por ID."""
        try:
            data = self._leer_json(self.hotel_data_file)
            reservas = data.get('reservas', [])
            
            for r in reservas:
                if r['id'] == id_reserva:
                    return Reserva.from_dict(r)
            return None
        except Exception as e:
            print(f"Error al obtener reserva: {e}")
            return None
    
    def obtener_todas_reservas(self) -> List[Reserva]:
        """Obtiene todas las reservas."""
        try:
            data = self._leer_json(self.hotel_data_file)
            reservas = data.get('reservas', [])
            return [Reserva.from_dict(r) for r in reservas]
        except Exception as e:
            print(f"Error al obtener reservas: {e}")
            return []
    
    def obtener_reservas_cliente(self, cliente_id: str) -> List[Reserva]:
        """Obtiene todas las reservas de un cliente."""
        try:
            todas_reservas = self.obtener_todas_reservas()
            return [r for r in todas_reservas if r.cliente_id == cliente_id]
        except Exception as e:
            print(f"Error al obtener reservas del cliente: {e}")
            return []
    
    def generar_id_cliente(self) -> str:
        """Genera un nuevo ID de cliente."""
        try:
            data = self._leer_json(self.hotel_data_file)
            contador = data.get('contadores', {}).get('cliente', 1)
            nuevo_id = f"CLI{contador:04d}"
            
            data['contadores']['cliente'] = contador + 1
            self._guardar_json(self.hotel_data_file, data)
            
            return nuevo_id
        except Exception as e:
            print(f"Error al generar ID cliente: {e}")
            return f"CLI{datetime.now().timestamp()}"
    
    def generar_id_reserva(self) -> str:
        """Genera un nuevo ID de reserva."""
        try:
            data = self._leer_json(self.hotel_data_file)
            contador = data.get('contadores', {}).get('reserva', 1)
            nuevo_id = f"RES{contador:04d}"
            
            data['contadores']['reserva'] = contador + 1
            self._guardar_json(self.hotel_data_file, data)
            
            return nuevo_id
        except Exception as e:
            print(f"Error al generar ID reserva: {e}")
            return f"RES{datetime.now().timestamp()}"
