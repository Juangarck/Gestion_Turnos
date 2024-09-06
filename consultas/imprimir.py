from escpos.printer import Network
from datetime import datetime
import sys

# Configuración de la impresora
PRINTER_IP = "192.168.1.100"  # Cambia esta IP por la de tu impresora
PRINTER_PORT = 9100  # Puerto por defecto para impresoras de red

def print_console(nombre, cedula, turno):
    # Obtener la fecha y hora actual
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Imprimir en consola (simulación de impresión)
    print("          Digi Turno")  # Centrando el título
    print("               ")  # Línea vacía
    print(f"          Turno: {turno}")  # Centrando el turno
    print("---------------")
    print(f"Nombre: {nombre}")  # Alineado a la izquierda
    print(f"Cédula: {cedula}")  # Alineado a la izquierda
    print(f"                      {now}")  # Alineado a la derecha
    print("---------------")
    print("¡Gracias por su espera!")


def print_ticket(nombre, cedula, turno):
    # Conectarse a la impresora
    printer = Network(PRINTER_IP, PRINTER_PORT)
    
    # Obtener la fecha y hora actual
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Configurar los parámetros de la impresión
    printer.set(align='center', font='a', width=2, height=2)
    printer.text("Digi Turno\n")
    printer.text("---------------\n")
    printer.set(align='left', font='a', width=1, height=1)
    printer.text(f"Nombre: {nombre}\n")
    printer.text(f"Cédula: {cedula}\n")
    printer.text(f"Turno: {turno}\n")
    printer.text(f"Fecha y Hora: {now}\n")
    printer.text("---------------\n")
    printer.text("¡Gracias por su espera!\n")
    printer.cut()
    
    # Cerrar la conexión con la impresora
    printer.close()

def main():
    # Obtener parámetros de la línea de comandos
    if len(sys.argv) != 4:
        print("Uso: imprimir.py <nombre> <cedula> <turno>")
        sys.exit(1)

    nombre = sys.argv[1]
    cedula = sys.argv[2]
    turno = sys.argv[3]

    # Imprimir en consola (comentado para no ejecutar)
    print("IMPRIME CORRECTAMENTE: ")
    print_console(nombre, cedula, turno)
    
    # Imprimir en la impresora
    #print_ticket(nombre, cedula, turno)

if __name__ == "__main__":
    main()
