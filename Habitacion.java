ver habitaciones disponiblepackage model;

import java.util.Objects;

/**
 * Representa una habitación del hotel con sus características y disponibilidad.
 */
public class Habitacion {
    private String numero;
    private TipoHabitacion tipo;
    private double precioPorNoche;
    private int capacidadPersonas;
    private boolean disponible;
    private String descripcion;

    public enum TipoHabitacion {
        SIMPLE("Simple", 1),
        DOBLE("Doble", 2),
        SUITE("Suite", 4),
        PRESIDENCIAL("Presidencial", 6);

        private final String nombre;
        private final int capacidadMaxima;

        TipoHabitacion(String nombre, int capacidadMaxima) {
            this.nombre = nombre;
            this.capacidadMaxima = capacidadMaxima;
        }

        public String getNombre() {
            return nombre;
        }

        public int getCapacidadMaxima() {
            return capacidadMaxima;
        }

        public static TipoHabitacion desdeOpcionMenu(int opcion) {
            switch (opcion) {
                case 1:
                    return SIMPLE;
                case 2:
                    return DOBLE;
                case 3:
                    return SUITE;
                case 4:
                    return PRESIDENCIAL;
                default:
                    throw new IllegalArgumentException("Opción de tipo de habitación inválida: " + opcion);
            }
        }
    }

    public Habitacion(String numero, TipoHabitacion tipo, double precioPorNoche, 
                      int capacidadPersonas, String descripcion) {
        this.numero = numero;
        this.tipo = tipo;
        this.precioPorNoche = precioPorNoche;
        this.capacidadPersonas = capacidadPersonas;
        this.disponible = true;
        this.descripcion = descripcion;
    }

    public String getNumero() {
        return numero;
    }

    public void setNumero(String numero) {
        this.numero = numero;
    }

    public TipoHabitacion getTipo() {
        return tipo;
    }

    public void setTipo(TipoHabitacion tipo) {
        this.tipo = tipo;
    }

    public double getPrecioPorNoche() {
        return precioPorNoche;
    }

    public void setPrecioPorNoche(double precioPorNoche) {
        this.precioPorNoche = precioPorNoche;
    }

    public int getCapacidadPersonas() {
        return capacidadPersonas;
    }

    public void setCapacidadPersonas(int capacidadPersonas) {
        this.capacidadPersonas = capacidadPersonas;
    }

    public boolean isDisponible() {
        return disponible;
    }

    public void setDisponible(boolean disponible) {
        this.disponible = disponible;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Habitacion that = (Habitacion) o;
        return Objects.equals(numero, that.numero);
    }

    @Override
    public int hashCode() {
        return Objects.hash(numero);
    }

    @Override
    public String toString() {
        return "Habitacion{" +
                "numero='" + numero + '\'' +
                ", tipo=" + tipo.getNombre() +
                ", precio=$" + precioPorNoche +
                ", capacidad=" + capacidadPersonas +
                ", disponible=" + (disponible ? "Sí" : "No") +
                '}';
    }
}
