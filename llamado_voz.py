import pyttsx3
import json
import time
import sys

# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()

# Ajustar la velocidad y el volumen
engine.setProperty('rate', 140)  # Velocidad de 140 palabras por minuto
engine.setProperty('volume', 0.9)  # Volumen al 90%

# Selección de voz en español
voices = engine.getProperty('voices')
for voice in voices:
    if 'spanish' in voice.languages or 'es' in voice.id:
        if 'female' in voice.id or 'femenina' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            print(f"Usando la voz: {voice.name}")
            break

# Función para llamar turnos
def llamar_turno(turno, ventanilla, cliente):
    mensaje = f"Turno {turno}, favor dirigirse a la ventanilla {ventanilla}. Señor {cliente}, su turno está listo."
    print(mensaje)  # Mostrar en pantalla
    engine.say(mensaje)  # Reproducir en voz
    engine.runAndWait()  # Esperar a que termine la reproducción

# Verificar si los parámetros fueron pasados
if len(sys.argv) > 3:
    turno = sys.argv[1]
    ventanilla = sys.argv[2]
    cliente = sys.argv[3]
    llamar_turno(turno, ventanilla, cliente)
else:
    print("Faltan parámetros para el llamado de turno.")

# Finalizar el motor de síntesis
engine.stop()