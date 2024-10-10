import pyttsx3
import sys
import os

# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()

# Ajustar la velocidad y el volumen
engine.setProperty('rate', 140)  # Velocidad de 140 palabras por minuto
engine.setProperty('volume', 0.9)  # Volumen al 90%

# Selección de voz en español femenina
voices = engine.getProperty('voices')
for voice in voices:
    if 'spanish' in voice.languages or 'es' in voice.id:
        if 'female' in voice.id or 'femenina' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
# Función para eliminar el archivo del turno anterior
def eliminar_turno_anterior(num_turno):
    turno_anterior = int(num_turno) - 1
    archivo_anterior = f'tonos/turno_{turno_anterior}.ogg'
    if os.path.exists(archivo_anterior):
        os.remove(archivo_anterior)
        print(f"Archivo {archivo_anterior} eliminado.")
    else:
        print(f"No se encontró el archivo {archivo_anterior}.")

# Función para llamar turnos
def llamar_turno(num_turno, num_ventanilla, nom_cliente):
    mensaje = f"Turno {num_turno}, favor dirigirse a la ventanilla {num_ventanilla}. Usuario {nom_cliente}"
    print(mensaje)  # Mostrar en pantalla
    engine.say(mensaje)  # Reproducir en voz
    # Guardar el archivo de audio como .ogg
    engine.save_to_file(mensaje, f'tonos/turno_{num_turno}.ogg')
    engine.runAndWait()  # Esperar a que termine la reproducción

    # Llamar a la función para eliminar el archivo de turno anterior
    eliminar_turno_anterior(num_turno)

# Verificar si los parámetros fueron pasados correctamente
if len(sys.argv) > 3:
    num_turno = sys.argv[1]
    num_ventanilla = sys.argv[2]
    nom_cliente = sys.argv[3]
    llamar_turno(num_turno, num_ventanilla, nom_cliente)
else:
    print("Faltan parámetros para el llamado de turno.")

# Finalizar el motor de síntesis
engine.stop()