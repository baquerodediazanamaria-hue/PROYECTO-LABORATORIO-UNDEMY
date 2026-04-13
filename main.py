#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import date
from hotel import Hotel
from habitacion import TipoHabitacion
from utils import (
    leer_entero, leer_texto, confirmar_accion, mostrar_menu,
    pausar, parsear_fecha, formatear_fecha, formatear_dinero
)

class SistemaHotelCLI:
    """Interfaz CLI para el Sistema de Gestión Hotelera."""
    
    def __init__(self):
        self.hotel = Hotel("Hotel Grand Paradise")
        self.ejecutando = True
    
    def ejecutar(self):
        """Ejecuta el sistema."""
        self.mostrar_bienvenida()
        
        while self.ejecutando:
            try:
                self.menu_principal()
            except KeyboardInterrupt:
                print("\n\n✗ Operación cancelada por el usuario")
                if confirmar_accion("\n¿Desea salir del sistema? (S/N): "):
                    self.ejecutando = False
            except Exception as e:
                print(f"\n✗ Error inesperado: {e}")
                pausar()
        
        self.mostrar_despedida()
    
    def mostrar_bienvenida(self):
        """Muestra el mensaje de bienvenida."""
        print("\n" + "="*60)
        print("║" + " "*58 + "║")
        print("║" + "  SISTEMA DE GESTIÓN Y CHECK-IN HOTELERO - PYTHON CLI".center(58) + "║")
        print("║" + f"  {self.hotel.nombre}".center(58) + "║")
        print("║" + " "*58 + "║")
        print("="*60)
        print("\n✓ Sistema inicializado correctamente\n")
        pausar()
    
    def mostrar_despedida(self):
        """Muestra el mensaje de despedida."""
        print("\n" + "="*60)
        print("  ¡Gracias por usar el Sistema de Gestión Hotelera!  ")
        print("  " + self.hotel.nombre)
        print("="*60 + "\n")
    
    def menu_principal(self):
        """Menú principal del sistema."""
        opciones = [
            "Registrar Nuevo Cliente",
            "Buscar Cliente",
            "Listar Todos los Clientes",
            "Ver Habitaciones Disponibles",
            "Ver Habitaciones por Tipo",
            "Crear Nueva Reserva",
            "Consultar Reserva",
            "Ver Reservas de Cliente",
            "Realizar Check-in",
            "Realizar Check-out",
            "Cancelar Reserva",
            "Ver Reservas Activas",
            "Calcular Costo Estimado",
            "Estadísticas del Hotel"
        ]
        
        opcion = mostrar_menu("MENÚ PRINCIPAL", opciones)
        
        if opcion == 0:
            if confirmar_accion("\n¿Está seguro que desea salir? (S/N): "):
                self.ejecutando = False
        elif opcion == 1:
            self.registrar_cliente()
        elif opcion == 2:
            self.buscar_cliente()
        elif opcion == 3:
            self.listar_clientes()
        elif opcion == 4:
            self.ver_habitaciones_disponibles()
        elif opcion == 5:
            self.ver_habitaciones_por_tipo()
        elif opcion == 6:
            self.crear_reserva()
        elif opcion == 7:
            self.consultar_reserva()
        elif opcion == 8:
            self.ver_reservas_cliente()
        elif opcion == 9:
            self.realizar_checkin()
        elif opcion == 10:
            self.realizar_checkout()
        elif opcion == 11:
            self.cancelar_reserva()
        elif opcion == 12:
            self.ver_reservas_activas()
        elif opcion == 13:
            self.calcular_costo_estimado()
        elif opcion == 14:
            self.mostrar_estadisticas()
        else:
            print("\n✗ Opción inválida")
        
        if self.ejecutando and opcion != 0:
            pausar()
    
    def registrar_cliente(self):
        """Registra un nuevo cliente."""
        print("\n" + "="*60)
        print("  REGISTRAR NUEVO CLIENTE")
        print("="*60)
        
        try:
            nombre = leer_texto("Nombre: ")
            apellido = leer_texto("Apellido: ")
            documento = leer_texto("Documento (DNI/Pasaporte): ")
            email = leer_texto("Email: ", obligatorio=False)
            telefono = leer_texto("Teléfono: ")
            nacionalidad = leer_texto("Nacionalidad: ")
            
            cliente = self.hotel.registrar_cliente(
                nombre, apellido, documento, email, telefono, nacionalidad
            )
            
            if cliente:
                print("\n✓ Cliente registrado exitosamente!")
                print(f"  ID: {cliente.id}")
                print(f"  Nombre: {cliente.nombre_completo()}")
                print(f"  Documento: {cliente.documento}")
            else:
                print("\n✗ No se pudo registrar el cliente")
        
        except ValueError as e:
            print(f"\n✗ Error de validación: {e}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def buscar_cliente(self):
        """Busca un cliente por documento."""
        print("\n" + "="*60)
        print("  BUSCAR CLIENTE")
        print("="*60)
        
        documento = leer_texto("Ingrese documento: ")
        cliente = self.hotel.buscar_cliente(documento)
        
        if cliente:
            print("\n✓ Cliente encontrado:")
            self.mostrar_detalles_cliente(cliente)
        else:
            print("\n✗ No se encontró ningún cliente con ese documento")
    
    def listar_clientes(self):
        """Lista todos los clientes."""
        print("\n" + "="*60)
        print("  LISTA DE CLIENTES")
        print("="*60)
        
        clientes = self.hotel.obtener_todos_clientes()
        
        if not clientes:
            print("\n✗ No hay clientes registrados")
            return
        
        print(f"\nTotal de clientes: {len(clientes)}")
        print("-" * 60)
        
        for cliente in clientes:
            print(f"\nID: {cliente.id} | {cliente.nombre_completo()}")
            print(f"  Doc: {cliente.documento} | Tel: {cliente.telefono}")
    
    def ver_habitaciones_disponibles(self):
        """Muestra las habitaciones disponibles."""
        print("\n" + "="*60)
        print("  HABITACIONES DISPONIBLES")
        print("="*60)
        
        habitaciones = self.hotel.obtener_habitaciones_disponibles()
        
        if not habitaciones:
            print("\n✗ No hay habitaciones disponibles")
            return
        
        print(f"\nTotal disponibles: {len(habitaciones)}")
        print("-" * 60)
        
        for hab in habitaciones:
            print(f"\n  Habitación {hab.numero} - {hab.tipo.nombre_tipo}")
            print(f"  Precio: {formatear_dinero(hab.precio_por_noche)} por noche")
            print(f"  Capacidad: {hab.capacidad} persona(s)")
            print(f"  {hab.descripcion}")
    
    def ver_habitaciones_por_tipo(self):
        """Muestra habitaciones por tipo."""
        print("\n" + "="*60)
        print("  HABITACIONES POR TIPO")
        print("="*60)
        
        tipos = list(TipoHabitacion)
        print("\nTipos disponibles:")
        for i, tipo in enumerate(tipos, 1):
            print(f"{i}. {tipo.nombre_tipo}")
        
        opcion = leer_entero("\nSeleccione tipo: ", 1, len(tipos))
        tipo_seleccionado = tipos[opcion - 1]
        
        habitaciones = self.hotel.obtener_habitaciones_por_tipo(tipo_seleccionado)
        
        if not habitaciones:
            print(f"\n✗ No hay habitaciones disponibles de tipo {tipo_seleccionado.nombre_tipo}")
            return
        
        print(f"\nHabitaciones {tipo_seleccionado.nombre_tipo} disponibles:")
        print("-" * 60)
        
        for hab in habitaciones:
            print(f"\n  Habitación {hab.numero}")
            print(f"  {formatear_dinero(hab.precio_por_noche)}/noche - Capacidad: {hab.capacidad}")
            print(f"  {hab.descripcion}")
    
    def crear_reserva(self):
        """Crea una nueva reserva."""
        print("\n" + "="*60)
        print("  CREAR NUEVA RESERVA")
        print("="*60)
        
        try:
            documento = leer_texto("Documento del cliente: ")
            cliente = self.hotel.buscar_cliente(documento)
            
            if not cliente:
                print("\n✗ Cliente no encontrado. Debe registrarse primero.")
                return
            
            print(f"\n✓ Cliente: {cliente.nombre_completo()}")
            
            numero_hab = leer_texto("Número de habitación: ")
            habitacion = self.hotel.buscar_habitacion(numero_hab)
            
            if not habitacion:
                print("\n✗ Habitación no encontrada")
                return
            
            if not habitacion.disponible:
                print("\n✗ La habitación no está disponible")
                return
            
            print(f"\n✓ Habitación: {habitacion.numero} - {habitacion.tipo.nombre_tipo}")
            print(f"  {formatear_dinero(habitacion.precio_por_noche)}/noche")
            
            fecha_in_str = leer_texto("Fecha check-in (dd/mm/aaaa): ")
            fecha_in = parsear_fecha(fecha_in_str)
            
            if not fecha_in:
                print("\n✗ Formato de fecha inválido")
                return
            
            fecha_out_str = leer_texto("Fecha check-out (dd/mm/aaaa): ")
            fecha_out = parsear_fecha(fecha_out_str)
            
            if not fecha_out:
                print("\n✗ Formato de fecha inválido")
                return
            
            num_huespedes = leer_entero("Número de huéspedes: ", 1, habitacion.capacidad)
            notas = leer_texto("Notas adicionales (opcional): ", obligatorio=False)
            
            reserva = self.hotel.crear_reserva(
                documento, numero_hab, fecha_in, fecha_out, num_huespedes, notas
            )
            
            if reserva:
                print("\n✓ Reserva creada exitosamente!")
                self.mostrar_detalles_reserva(reserva, cliente, habitacion)
            else:
                print("\n✗ No se pudo crear la reserva")
        
        except ValueError as e:
            print(f"\n✗ Error de validación: {e}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def consultar_reserva(self):
        """Consulta una reserva por ID."""
        print("\n" + "="*60)
        print("  CONSULTAR RESERVA")
        print("="*60)
        
        id_reserva = leer_texto("ID de la reserva: ")
        reserva = self.hotel.buscar_reserva(id_reserva)
        
        if reserva:
            print("\n✓ Reserva encontrada:")
            cliente = self.hotel.buscar_cliente(
                next((c.documento for c in self.hotel.obtener_todos_clientes() 
                      if c.id == reserva.cliente_id), "")
            )
            habitacion = self.hotel.buscar_habitacion(reserva.habitacion_numero)
            self.mostrar_detalles_reserva(reserva, cliente, habitacion)
        else:
            print("\n✗ Reserva no encontrada")
    
    def ver_reservas_cliente(self):
        """Muestra las reservas de un cliente."""
        print("\n" + "="*60)
        print("  RESERVAS DE CLIENTE")
        print("="*60)
        
        documento = leer_texto("Documento del cliente: ")
        reservas = self.hotel.obtener_reservas_cliente(documento)
        
        if not reservas:
            print("\n✗ El cliente no tiene reservas")
            return
        
        print(f"\nTotal de reservas: {len(reservas)}")
        print("-" * 60)
        
        for reserva in reservas:
            habitacion = self.hotel.buscar_habitacion(reserva.habitacion_numero)
            print(f"\nReserva {reserva.id} - {reserva.estado.value}")
            print(f"  Habitación: {reserva.habitacion_numero}")
            print(f"  Check-in: {formatear_fecha(reserva.fecha_checkin)}")
            print(f"  Check-out: {formatear_fecha(reserva.fecha_checkout)}")
            print(f"  Costo: {formatear_dinero(reserva.costo_total)}")
    
    def realizar_checkin(self):
        """Realiza el check-in de una reserva."""
        print("\n" + "="*60)
        print("  REALIZAR CHECK-IN")
        print("="*60)
        
        id_reserva = leer_texto("ID de la reserva: ")
        
        if self.hotel.realizar_checkin(id_reserva):
            print("\n✓ Check-in realizado exitosamente!")
            print("  Estado: EN CURSO")
        else:
            print("\n✗ No se pudo realizar el check-in")
    
    def realizar_checkout(self):
        """Realiza el check-out de una reserva."""
        print("\n" + "="*60)
        print("  REALIZAR CHECK-OUT")
        print("="*60)
        
        id_reserva = leer_texto("ID de la reserva: ")
        costo = self.hotel.realizar_checkout(id_reserva)
        
        if costo is not None:
            print("\n✓ Check-out realizado exitosamente!")
            print(f"  Costo Total: {formatear_dinero(costo)}")
            print("  ¡Gracias por hospedarse con nosotros!")
        else:
            print("\n✗ No se pudo realizar el check-out")
    
    def cancelar_reserva(self):
        """Cancela una reserva."""
        print("\n" + "="*60)
        print("  CANCELAR RESERVA")
        print("="*60)
        
        id_reserva = leer_texto("ID de la reserva: ")
        
        if confirmar_accion("\n¿Está seguro de cancelar esta reserva? (S/N): "):
            if self.hotel.cancelar_reserva(id_reserva):
                print("\n✓ Reserva cancelada exitosamente")
            else:
                print("\n✗ No se pudo cancelar la reserva")
        else:
            print("\n✗ Cancelación abortada")
    
    def ver_reservas_activas(self):
        """Muestra las reservas activas."""
        print("\n" + "="*60)
        print("  RESERVAS ACTIVAS")
        print("="*60)
        
        reservas = self.hotel.obtener_reservas_activas()
        
        if not reservas:
            print("\n✗ No hay reservas activas")
            return
        
        print(f"\nTotal de reservas activas: {len(reservas)}")
        print("-" * 60)
        
        for reserva in reservas:
            print(f"\nReserva {reserva.id} - {reserva.estado.value}")
            print(f"  Habitación: {reserva.habitacion_numero}")
            print(f"  Check-in: {formatear_fecha(reserva.fecha_checkin)}")
            print(f"  Check-out: {formatear_fecha(reserva.fecha_checkout)}")
    
    def calcular_costo_estimado(self):
        """Calcula el costo estimado de una estancia."""
        print("\n" + "="*60)
        print("  CALCULAR COSTO ESTIMADO")
        print("="*60)
        
        tipos = list(TipoHabitacion)
        print("\nTipos de habitación:")
        for i, tipo in enumerate(tipos, 1):
            print(f"{i}. {tipo.nombre_tipo} - {formatear_dinero(tipo.precio_base)}/noche")
        
        opcion = leer_entero("\nSeleccione tipo: ", 1, len(tipos))
        tipo_seleccionado = tipos[opcion - 1]
        
        num_noches = leer_entero("Número de noches: ", 1)
        
        costo = self.hotel.calcular_costo_estimado(tipo_seleccionado, num_noches)
        
        print("\n" + "="*60)
        print("  ESTIMACIÓN DE COSTO")
        print("="*60)
        print(f"\nTipo: {tipo_seleccionado.nombre_tipo}")
        print(f"Noches: {num_noches}")
        print(f"Precio por noche: {formatear_dinero(tipo_seleccionado.precio_base)}")
        print(f"\nCosto Total Estimado: {formatear_dinero(costo)}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del hotel."""
        print("\n" + "="*60)
        print("  ESTADÍSTICAS DEL HOTEL")
        print("="*60)
        
        stats = self.hotel.obtener_estadisticas()
        
        print(f"\n  Total de clientes: {stats['total_clientes']}")
        print(f"  Total de habitaciones: {stats['total_habitaciones']}")
        print(f"  Habitaciones disponibles: {stats['habitaciones_disponibles']}")
        print(f"  Habitaciones ocupadas: {stats['habitaciones_ocupadas']}")
        print(f"  Total de reservas: {stats['total_reservas']}")
        print(f"  Reservas activas: {stats['reservas_activas']}")
        print(f"  Tasa de ocupación: {stats['tasa_ocupacion']:.1f}%")
    
    def mostrar_detalles_cliente(self, cliente):
        """Muestra los detalles de un cliente."""
        print("-" * 60)
        print(f"  ID: {cliente.id}")
        print(f"  Nombre: {cliente.nombre_completo()}")
        print(f"  Documento: {cliente.documento}")
        print(f"  Email: {cliente.email}")
        print(f"  Teléfono: {cliente.telefono}")
        print(f"  Nacionalidad: {cliente.nacionalidad}")
        print("-" * 60)
    
    def mostrar_detalles_reserva(self, reserva, cliente=None, habitacion=None):
        """Muestra los detalles de una reserva."""
        print("-" * 60)
        print(f"  ID Reserva: {reserva.id}")
        if cliente:
            print(f"  Cliente: {cliente.nombre_completo()}")
        print(f"  Habitación: {reserva.habitacion_numero}", end="")
        if habitacion:
            print(f" ({habitacion.tipo.nombre_tipo})")
        else:
            print()
        print(f"  Check-in: {formatear_fecha(reserva.fecha_checkin)}")
        print(f"  Check-out: {formatear_fecha(reserva.fecha_checkout)}")
        print(f"  Noches: {reserva.calcular_numero_noches()}")
        print(f"  Huéspedes: {reserva.numero_huespedes}")
        print(f"  Costo Total: {formatear_dinero(reserva.costo_total)}")
        print(f"  Estado: {reserva.estado.value}")
        if reserva.notas:
            print(f"  Notas: {reserva.notas}")
        print("-" * 60)


def main():
    """Función principal."""
    try:
        sistema = SistemaHotelCLI()
        sistema.ejecutar()
    except KeyboardInterrupt:
        print("\n\n✗ Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
