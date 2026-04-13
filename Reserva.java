package model;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.Objects;

/**
 * Representa una reserva de habitación con información del cliente y fechas.
 */
public class Reserva {
    private String id;
    private Cliente cliente;
    private Habitacion habitacion;
    private LocalDate fechaCheckIn;
    private LocalDate fechaCheckOut;
    private int numeroDias;
    private double costoTotal;
    private EstadoReserva estado;

    public enum EstadoReserva {
        PENDIENTE("Pendiente"),
        CONFIRMADA("Confirmada"),
        EN_CURSO("En Curso"),
        FINALIZADA("Finalizada"),
        CANCELADA("Cancelada");

        private final String descripcion;

        EstadoReserva(String descripcion) {
            this.descripcion = descripcion;
        }

        public String getDescripcion() {
            return descripcion;
        }
    }

    public Reserva(String id, Cliente cliente, Habitacion habitacion, 
                   LocalDate fechaCheckIn, LocalDate fechaCheckOut) {
        this.id = id;
        this.cliente = cliente;
        this.habitacion = habitacion;
        this.fechaCheckIn = fechaCheckIn;
        this.fechaCheckOut = fechaCheckOut;
        this.numeroDias = calcularDias();
        this.costoTotal = calcularCostoTotal();
        this.estado = EstadoReserva.PENDIENTE;
    }

    private int calcularDias() {
        return (int) ChronoUnit.DAYS.between(fechaCheckIn, fechaCheckOut);
    }

    private double calcularCostoTotal() {
        return numeroDias * habitacion.getPrecioPorNoche();
    }

    public void recalcularCosto() {
        this.numeroDias = calcularDias();
        this.costoTotal = calcularCostoTotal();
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Cliente getCliente() {
        return cliente;
    }

    public void setCliente(Cliente cliente) {
        this.cliente = cliente;
    }

    public Habitacion getHabitacion() {
        return habitacion;
    }

    public void setHabitacion(Habitacion habitacion) {
        this.habitacion = habitacion;
        recalcularCosto();
    }

    public LocalDate getFechaCheckIn() {
        return fechaCheckIn;
    }

    public void setFechaCheckIn(LocalDate fechaCheckIn) {
        this.fechaCheckIn = fechaCheckIn;
        recalcularCosto();
    }

    public LocalDate getFechaCheckOut() {
        return fechaCheckOut;
    }

    public void setFechaCheckOut(LocalDate fechaCheckOut) {
        this.fechaCheckOut = fechaCheckOut;
        recalcularCosto();
    }

    public int getNumeroDias() {
        return numeroDias;
    }

    public double getCostoTotal() {
        return costoTotal;
    }

    public EstadoReserva getEstado() {
        return estado;
    }

    public void setEstado(EstadoReserva estado) {
        this.estado = estado;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Reserva reserva = (Reserva) o;
        return Objects.equals(id, reserva.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "Reserva{" +
                "id='" + id + '\'' +
                ", cliente=" + cliente.getNombreCompleto() +
                ", habitacion=" + habitacion.getNumero() +
                ", checkIn=" + fechaCheckIn +
                ", checkOut=" + fechaCheckOut +
                ", dias=" + numeroDias +
                ", total=$" + costoTotal +
                ", estado=" + estado.getDescripcion() +
                '}';
    }
}
