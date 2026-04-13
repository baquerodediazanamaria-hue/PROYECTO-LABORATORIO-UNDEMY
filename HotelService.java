package service;

import data.BaseDatosHotel;
import model.Cliente;
import model.Habitacion;
import model.Habitacion.TipoHabitacion;
import model.Reserva;
import model.Reserva.EstadoReserva;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

/**
 * Servicio principal con la lógica de negocio del sistema hotelero.
 */
public class HotelService {

    public String registrarCliente(String nombre, String apellido, String documento, 
                                   String email, String telefono, String nacionalidad) 
            throws IllegalArgumentException {
        
        if (nombre == null || nombre.trim().isEmpty()) {
            throw new IllegalArgumentException("El nombre no puede estar vacío");
        }
        if (apellido == null || apellido.trim().isEmpty()) {
            throw new IllegalArgumentException("El apellido no puede estar vacío");
        }
        if (documento == null || documento.trim().isEmpty()) {
            throw new IllegalArgumentException("El documento no puede estar vacío");
        }

        Optional<Cliente> existente = BaseDatosHotel.buscarClientePorDocumento(documento);
        if (existente.isPresent()) {
            throw new IllegalArgumentException("Ya existe un cliente con ese documento");
        }

        String id = BaseDatosHotel.generarIdCliente();
        Cliente cliente = new Cliente(id, nombre.trim(), apellido.trim(), documento.trim(), 
                                     email.trim(), telefono.trim(), nacionalidad.trim());
        BaseDatosHotel.agregarCliente(cliente);
        
        return id;
    }

    public Optional<Cliente> buscarCliente(String documento) {
        if (documento == null || documento.trim().isEmpty()) {
            return Optional.empty();
        }
        return BaseDatosHotel.buscarClientePorDocumento(documento.trim());
    }

    public List<Habitacion> consultarHabitacionesDisponibles() {
        return BaseDatosHotel.obtenerHabitacionesDisponibles();
    }

    public List<Habitacion> consultarHabitacionesPorTipo(TipoHabitacion tipo) {
        return BaseDatosHotel.obtenerHabitacionesPorTipo(tipo);
    }

    public String crearReserva(String documentoCliente, String numeroHabitacion, 
                              LocalDate fechaCheckIn, LocalDate fechaCheckOut) 
            throws IllegalArgumentException {
        
        if (fechaCheckIn == null || fechaCheckOut == null) {
            throw new IllegalArgumentException("Las fechas no pueden ser nulas");
        }

        if (fechaCheckIn.isAfter(fechaCheckOut) || fechaCheckIn.isEqual(fechaCheckOut)) {
            throw new IllegalArgumentException("La fecha de check-in debe ser anterior al check-out");
        }

        if (fechaCheckIn.isBefore(LocalDate.now())) {
            throw new IllegalArgumentException("La fecha de check-in no puede ser anterior a hoy");
        }

        Optional<Cliente> clienteOpt = BaseDatosHotel.buscarClientePorDocumento(documentoCliente);
        if (!clienteOpt.isPresent()) {
            throw new IllegalArgumentException("Cliente no encontrado");
        }

        Optional<Habitacion> habitacionOpt = BaseDatosHotel.buscarHabitacionPorNumero(numeroHabitacion);
        if (!habitacionOpt.isPresent()) {
            throw new IllegalArgumentException("Habitación no encontrada");
        }

        Habitacion habitacion = habitacionOpt.get();
        if (!habitacion.isDisponible()) {
            throw new IllegalArgumentException("La habitación no está disponible");
        }

        String idReserva = BaseDatosHotel.generarIdReserva();
        Reserva reserva = new Reserva(idReserva, clienteOpt.get(), habitacion, 
                                     fechaCheckIn, fechaCheckOut);
        reserva.setEstado(EstadoReserva.CONFIRMADA);
        
        habitacion.setDisponible(false);
        BaseDatosHotel.agregarReserva(reserva);

        return idReserva;
    }

    public void realizarCheckIn(String idReserva) throws IllegalArgumentException {
        Optional<Reserva> reservaOpt = BaseDatosHotel.buscarReservaPorId(idReserva);
        
        if (!reservaOpt.isPresent()) {
            throw new IllegalArgumentException("Reserva no encontrada");
        }

        Reserva reserva = reservaOpt.get();
        
        if (reserva.getEstado() != EstadoReserva.CONFIRMADA) {
            throw new IllegalArgumentException("La reserva no está en estado CONFIRMADA");
        }

        if (LocalDate.now().isBefore(reserva.getFechaCheckIn())) {
            throw new IllegalArgumentException("No se puede hacer check-in antes de la fecha programada");
        }

        reserva.setEstado(EstadoReserva.EN_CURSO);
    }

    public double realizarCheckOut(String idReserva) throws IllegalArgumentException {
        Optional<Reserva> reservaOpt = BaseDatosHotel.buscarReservaPorId(idReserva);
        
        if (!reservaOpt.isPresent()) {
            throw new IllegalArgumentException("Reserva no encontrada");
        }

        Reserva reserva = reservaOpt.get();
        
        if (reserva.getEstado() != EstadoReserva.EN_CURSO) {
            throw new IllegalArgumentException("La reserva no está en curso");
        }

        reserva.setEstado(EstadoReserva.FINALIZADA);
        reserva.getHabitacion().setDisponible(true);

        return reserva.getCostoTotal();
    }

    public void cancelarReserva(String idReserva) throws IllegalArgumentException {
        Optional<Reserva> reservaOpt = BaseDatosHotel.buscarReservaPorId(idReserva);
        
        if (!reservaOpt.isPresent()) {
            throw new IllegalArgumentException("Reserva no encontrada");
        }

        Reserva reserva = reservaOpt.get();
        
        if (reserva.getEstado() == EstadoReserva.FINALIZADA) {
            throw new IllegalArgumentException("No se puede cancelar una reserva finalizada");
        }

        reserva.setEstado(EstadoReserva.CANCELADA);
        reserva.getHabitacion().setDisponible(true);
    }

    public List<Reserva> consultarReservasCliente(String documentoCliente) {
        return BaseDatosHotel.obtenerReservasPorCliente(documentoCliente);
    }

    public Optional<Reserva> consultarReserva(String idReserva) {
        return BaseDatosHotel.buscarReservaPorId(idReserva);
    }

    public List<Reserva> consultarReservasActivas() {
        return BaseDatosHotel.obtenerReservasActivas();
    }

    public double calcularCostoReserva(TipoHabitacion tipo, int numeroDias) {
        List<Habitacion> habitaciones = BaseDatosHotel.obtenerHabitacionesPorTipo(tipo);
        if (habitaciones.isEmpty()) {
            return 0.0;
        }
        return habitaciones.get(0).getPrecioPorNoche() * numeroDias;
    }

    public List<Cliente> obtenerTodosClientes() {
        return BaseDatosHotel.obtenerTodosClientes();
    }

    public int obtenerEstadisticaClientes() {
        return BaseDatosHotel.getCantidadClientes();
    }

    public int obtenerEstadisticaReservas() {
        return BaseDatosHotel.getCantidadReservas();
    }

    public int obtenerEstadisticaHabitacionesDisponibles() {
        return (int) BaseDatosHotel.obtenerHabitacionesDisponibles().stream().count();
    }
}
