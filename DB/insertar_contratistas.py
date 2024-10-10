import pymysql
import random
import string
import unicodedata
from datetime import datetime

# Función para normalizar nombres (quita acentos, convierte a minúsculas)
def normalizar_texto(texto):
    # Normaliza quitando tildes y otros caracteres especiales
    texto_normalizado = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')
    # Convierte a minúsculas
    return texto_normalizado.lower()

# Función para generar nombre de usuario
def generar_usuario(nombre, apellido):
    # Normaliza y toma las primeras 3 letras del primer nombre y del primer apellido y agrega un número aleatorio entre 10 y 99
    usuario = (normalizar_texto(nombre).split()[0][:3] + normalizar_texto(apellido).split()[0][:3] + str(random.randint(10, 99)))
    return usuario

# Función para generar contraseña segura
def generar_contraseña(nombre, apellido):
    # Normaliza los nombres
    nombre_normalizado = normalizar_texto(nombre)
    apellido_normalizado = normalizar_texto(apellido)
    # Toma las primeras 2 letras del primer nombre y la inicial del primer apellido
    base = nombre_normalizado.split()[0][:2].capitalize() + apellido_normalizado.split()[0][0].capitalize()
    # Agrega números y caracteres especiales
    numeros = ''.join(random.choices(string.digits, k=3))
    caracteres_especiales = ''.join(random.choices('!@#$%^&*', k=2))
    # Combina todo para crear la contraseña
    return base + numeros + caracteres_especiales

# Función para insertar usuario en la base de datos
def insertar_usuario(nombre, apellido, connection):
    try:
        usuario = generar_usuario(nombre, apellido)
        contraseña = generar_contraseña(nombre, apellido)
        fecha_alta = datetime.now()
        fecha_actualizacion = fecha_alta

        with connection.cursor() as cursor:
            sql = "INSERT INTO usuarios (usuario, password, fecha_alta, fecha_actualizacion) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (usuario, contraseña, fecha_alta, fecha_actualizacion))
            connection.commit()
            print(f"Usuario {usuario} insertado correctamente.")
            print(f"Usuario: {usuario}, Contraseña: {contraseña}")
    except pymysql.MySQLError as e:
        print(f"Error al insertar el usuario: {e}")

# Conexión a la base de datos
def conectar_db():
    try:
        return pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='turnero'
        )
    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Lista de contratistas
contratistas = [
    {"nombre": "DUBAN ORLANDO", "apellido": "QUEVEDO PARDO"},
    {"nombre": "SANDRA MILENA", "apellido": "ACEVEDO FAJARDO"},
    {"nombre": "José Albeiro", "apellido": "Cardona Duque"},
    {"nombre": "EDWIN SEBASTIAN", "apellido": "GUERRERO GUERRERO"},
    {"nombre": "HERNAN", "apellido": "HERNANDEZ"},
    {"nombre": "YEISON", "apellido": "BETANCOUR"},
    {"nombre": "LINA MARIA", "apellido": "GONZALEZ VARGAS"},
    {"nombre": "MARIA MARGARITA", "apellido": "CABALLERO PEDROZA"},
    {"nombre": "WILLIAN RICARDO", "apellido": "CHAPARRO ZORRO"},
    {"nombre": "CIRO ALFONSO", "apellido": "VIZCAINO CARDENAS"},
    {"nombre": "KAREN LORENA", "apellido": "BÁEZ TORRES"},
    {"nombre": "MICHAEL STEVEN", "apellido": "RAMIREZ VARGAS"},
    {"nombre": "JOHN JAIRO", "apellido": "SANCHEZ MORALES"},
    {"nombre": "Joseph Jhoan", "apellido": "Mancera Mendieta"},
    {"nombre": "LUISA FERNANDA", "apellido": "CIFUENTES BONILLA"},
    {"nombre": "LUISA FERNANDA", "apellido": "PINZON MARTIN"}
]

# Ejecución del script
if __name__ == "__main__":
    connection = conectar_db()

    if connection:
        for contratista in contratistas:
            insertar_usuario(contratista['nombre'], contratista['apellido'], connection)

        connection.close()