import pymysql
import csv

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

# Leer los primeros 10 registros del CSV
def leer_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        registros = []
        for index, row in enumerate(reader):
            if index >= 1010:  # Limitar a los primeros 1010 registros para prueba
                break
            registros.append(row)
        return registros

# Eliminar duplicados por documento_identidad
def eliminar_duplicados(registros):
    vistos = set()
    registros_unicos = []
    for registro in registros:
        doc_id = registro['documento_identidad']
        if doc_id not in vistos:
            vistos.add(doc_id)
            registros_unicos.append(registro)
    return registros_unicos

# Insertar registros únicos en MySQL en lotes
def insertar_en_mysql_por_lotes(conn, registros, batch_size=5):
    cursor = conn.cursor()
    query = """
        INSERT INTO clientes (nombre, cedula, telefono, email, municipio, direccion, fechaRegistro, autorizacion)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), TRUE)
        ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
    """
    
    batch = []  # Lote para agrupar las inserciones
    for registro in registros:
        nombre = f"{registro['primer_nombre']} {registro['segundo_nombre']} {registro['primer_apellido']} {registro['segundo_apellido']}".strip()
        cedula = registro['documento_identidad']
        
        # Agregar cada registro al lote
        batch.append((nombre, cedula, None, None, None, None))
        
        # Si el lote alcanza el tamaño establecido, lo insertamos
        if len(batch) == batch_size:
            try:
                cursor.executemany(query, batch)
                conn.commit()  # Confirmamos la transacción
                print(f"Insertados {len(batch)} registros.")
            except pymysql.MySQLError as e:
                print(f"Error al insertar el lote: {e}")
            batch.clear()  # Vaciamos el lote para el siguiente grupo

    # Insertar los registros restantes si quedan menos de 'batch_size'
    if batch:
        try:
            cursor.executemany(query, batch)
            conn.commit()
            print(f"Insertados los últimos {len(batch)} registros.")
        except pymysql.MySQLError as e:
            print(f"Error al insertar el último lote: {e}")

# Script principal
def main():
    conn = conectar_db()
    if not conn:
        return

    file_path = 'C:/ACC/DB_TURNERO/db_usuarios_unicos.csv'
    registros = leer_csv(file_path)
    registros_unicos = eliminar_duplicados(registros)

    insertar_en_mysql_por_lotes(conn, registros_unicos, batch_size=5)  # Inserción por lotes de 5 registros

    conn.close()
    print("Proceso finalizado con éxito.")

if __name__ == "__main__":
    main()
