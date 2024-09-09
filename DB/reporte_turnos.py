import pymysql
import pandas as pd
from datetime import datetime, timedelta
import smtplib
import xlsxwriter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from openpyxl import load_workbook

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

def obtener_indicadores_por_usuario(conn):
    cursor = conn.cursor()
    
    # 1. Turnos atendidos por usuario por día
    query_turnos = """
    SELECT a.idCaja, u.usuario, DATE(fechaAtencion) as fecha, COUNT(*) as turnos_atendidos
    FROM atencion a
    JOIN usuarios u ON a.idCaja = u.idCaja
    WHERE DATE(fechaAtencion) = CURDATE()
    GROUP BY idCaja, DATE(fechaAtencion)
    """
    cursor.execute(query_turnos)
    turnos = cursor.fetchall()
    print("Turnos Atendidos:", turnos)  # Debugging output
    
    # 2. Tiempo promedio de espera de los clientes por día por cajera y global
    query_tiempo = """
    (SELECT a.idCaja, AVG(TIMESTAMPDIFF(MINUTE, t.fechaRegistro, a.fechaAtencion)) as tiempo_promedio
    FROM atencion a
    JOIN turnos t ON a.turno = t.turno
    WHERE DATE(a.fechaAtencion) = CURDATE()
    GROUP BY a.idCaja)

    UNION ALL

    (SELECT 'GLOBAL' as idCaja, AVG(TIMESTAMPDIFF(MINUTE, t.fechaRegistro, a.fechaAtencion)) as tiempo_promedio
    FROM atencion a
    JOIN turnos t ON a.turno = t.turno
    WHERE DATE(a.fechaAtencion) = CURDATE())
    """
    cursor.execute(query_tiempo)
    tiempos = cursor.fetchall()
    print("Tiempos Promedio:", tiempos)  # Debugging output
    
    # 3. Hora con mayor atención de turnos
    # 3.1. Hora de mayor atención de turnos por cajera
    query_hora_por_cajera = """
    SELECT a.idCaja, u.usuario, HOUR(a.fechaAtencion) as hora, COUNT(*) as turnos_atendidos
    FROM atencion a
    JOIN usuarios u ON a.idCaja = u.idCaja
    WHERE DATE(a.fechaAtencion) = CURDATE()
    GROUP BY a.idCaja, HOUR(a.fechaAtencion)
    ORDER BY a.idCaja, turnos_atendidos DESC
    """
    cursor.execute(query_hora_por_cajera)
    hora_pico_por_cajera = cursor.fetchall()

    # 3.2. Hora de mayor atención a nivel global
    query_hora_global = """
    SELECT HOUR(a.fechaAtencion) as hora, COUNT(*) as turnos_atendidos
    FROM atencion a
    WHERE DATE(a.fechaAtencion) = CURDATE()
    GROUP BY HOUR(a.fechaAtencion)
    ORDER BY turnos_atendidos DESC
    LIMIT 1
    """
    cursor.execute(query_hora_global)
    hora_pico_global = cursor.fetchone()

    # 4. Cantidad total de clientes atendidos y tiempo promedio de espera por día
    query_total_clientes_y_tiempo = """
    SELECT COUNT(*) as total_clientes,
        AVG(TIMESTAMPDIFF(MINUTE, t.fechaRegistro, a.fechaAtencion)) as tiempo_promedio_espera
    FROM atencion a
    JOIN turnos t ON a.turno = t.turno
    WHERE DATE(a.fechaAtencion) = CURDATE()
    """
    cursor.execute(query_total_clientes_y_tiempo)
    total_clientes_tiempo = cursor.fetchone()

    return turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo

def generar_reporte(turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo):
    # Crear un nuevo archivo Excel
    workbook = xlsxwriter.Workbook('reporte_turnos.xlsx')
    worksheet = workbook.add_worksheet()

    # Encabezados
    worksheet.write(0, 0, 'Usuario ID')
    worksheet.write(0, 1, 'Ventanilla')
    worksheet.write(0, 2, 'Fecha')
    worksheet.write(0, 3, 'Turnos Atendidos')
    worksheet.write(0, 4, 'Tiempo Promedio (minutos)')
    worksheet.write(0, 5, 'Hora Pico')
    worksheet.write(0, 6, 'Turnos en Hora Pico')

    # Llenar los datos de Turnos Atendidos
    row = 1
    for turno in turnos:
        worksheet.write(row, 0, turno[0])  # Usuario ID
        worksheet.write(row, 1, turno[1])  # Usuario
        worksheet.write(row, 2, str(turno[2]))  # Fecha
        worksheet.write(row, 3, turno[3])  # Turnos Atendidos
        row += 1

    # Llenar los datos de Tiempos Promedio
    row = 1
    for tiempo in tiempos:
        worksheet.write(row, 4, float(tiempo[1]))  # Tiempo Promedio en minutos
        row += 1

    # Llenar los datos de Hora Pico por cajera
    row = 1
    for hora in hora_pico_por_cajera:
        worksheet.write(row, 5, hora[2])  # Hora Pico
        worksheet.write(row, 6, hora[3])  # Turnos en Hora Pico
        row += 1

    # Saltar dos filas para las cifras globales
    row += 2
    worksheet.write(row, 0, 'Hora Pico Global')
    worksheet.write(row, 1, hora_pico_global[0])  # Hora Pico Global
    worksheet.write(row + 1, 0, 'Turnos en Hora Pico Global')
    worksheet.write(row + 1, 1, hora_pico_global[1])  # Turnos en Hora Pico Global

    # Llenar los datos de total de clientes atendidos y tiempo promedio
    worksheet.write(row + 3, 0, 'Total Clientes Atendidos')
    worksheet.write(row + 3, 1, total_clientes_tiempo[0])  # Total Clientes Atendidos
    worksheet.write(row + 4, 0, 'Tiempo Promedio de Espera (min)')
    worksheet.write(row + 4, 1, total_clientes_tiempo[1])  # Tiempo Promedio de Espera

    workbook.close()
    return 'reporte_turnos.xlsx'


def enviar_correo(reporte_path):
    from_address = 'juangarciagrracc@gmail.com'
    to_address = 'destinatario@correo.com'
    subject = 'Reporte de Turnos del Día'
    body = 'Adjunto el reporte de turnos del día con indicadores de rendimiento.'

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(reporte_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(reporte_path)}")
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, 'tu_contraseña')
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()

if __name__ == "__main__":
    conn = conectar_db()
    if conn:
        turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo = obtener_indicadores_por_usuario(conn)
        reporte_path = generar_reporte(turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo)
        #enviar_correo(reporte_path)  # Enviar el correo con el archivo adjunto
        conn.close()

