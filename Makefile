# Variables
JC = javac
JVM = java
BIN = bin
SRC = src

# Comando por defecto: Compila todo
all:
	mkdir -p $(BIN)
	$(JC) -d $(BIN) $(SRC)/model/*.java $(SRC)/data/*.java $(SRC)/service/*.java $(SRC)/SistemaHotel.java

# Ejecuta el sistema principal
run: all
	$(JVM) -cp $(BIN) SistemaHotel

# Limpia los archivos compilados
clean:
	rm -rf $(BIN)/*

# Recargar (limpiar y compilar)
reload: clean all