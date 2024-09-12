import pymysql
import smtplib
import xlsxwriter
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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

def generar_reporte(turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo, tipo_reporte, rango_fechas=None):
    reporte_nombre = f'reporte_turnos_{tipo_reporte}.xlsx'
    workbook = xlsxwriter.Workbook(reporte_nombre)
    worksheet = workbook.add_worksheet()

    formato_bold_centrado = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
    formato_centrado = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    formato_bordes = workbook.add_format({'border': 1})

    imagen_path = 'C:/xampp/htdocs/turnero/img/49550310_598832710562102_5995102219237874750_n.jpg'
    if os.path.exists(imagen_path):
        worksheet.merge_range('A1:A2', '', formato_centrado)
        worksheet.insert_image('A1', imagen_path, {'x_offset': 20, 'y_offset': 2, 'x_scale': 0.25, 'y_scale': 0.30})
    else:
        print(f"Advertencia: La imagen en '{imagen_path}' no se encontró.")

    total_columnas = 7
    columna_combinada = f'B1:{chr(65 + total_columnas - 1)}1'
    worksheet.merge_range(columna_combinada, 'AGENCIA CATASTRAL DE CUNDINAMARCA', formato_bold_centrado)

    columna_combinada2 = f'B2:{chr(65 + total_columnas - 1)}2'
    worksheet.merge_range(columna_combinada2, 'INFORME DE RENDIMIENTOS ATENCIÓN DE USUARIOS', formato_centrado)

    worksheet.write(2, 0, 'Usuario ID')
    worksheet.write(2, 1, 'Funcionario')
    worksheet.write(2, 2, 'Fecha' if tipo_reporte == 'diario' else f'Rango de Fechas ({rango_fechas})')
    worksheet.write(2, 3, 'Turnos Atendidos')
    worksheet.write(2, 4, 'Tiempo Promedio (espera mn)')
    worksheet.write(2, 5, 'Hora Pico')
    worksheet.write(2, 6, 'Turnos en Hora Pico')

    row = 3
    if turnos:
        for turno in turnos:
            worksheet.write(row, 0, turno[0])
            worksheet.write(row, 1, turno[1])
            worksheet.write(row, 2, str(turno[2]))
            worksheet.write(row, 3, turno[3])
            row += 1

    if tiempos:
        row = 3
        for tiempo in tiempos:
            worksheet.write(row, 4, float(tiempo[1]))
            row += 1

    if hora_pico_por_cajera:
        row = 3
        for hora in hora_pico_por_cajera:
            worksheet.write(row, 5, hora[2])
            worksheet.write(row, 6, hora[3])
            row += 1

    row += 2
    worksheet.write(row, 0, 'Hora Pico Global')
    worksheet.write(row, 1, hora_pico_global[0])
    worksheet.write(row + 1, 0, 'Turnos en Hora Pico Global')
    worksheet.write(row + 1, 1, hora_pico_global[1])

    worksheet.write(row + 3, 0, 'Total Clientes Atendidos')
    worksheet.write(row + 3, 1, total_clientes_tiempo[0])
    worksheet.write(row + 4, 0, 'Tiempo Promedio de Espera (min)')
    worksheet.write(row + 4, 1, total_clientes_tiempo[1])

    max_row = row + 4
    max_col = total_columnas - 1
    for r in range(2, max_row + 1):
        for c in range(max_col + 1):
            worksheet.write(r, c, '')

    # Ajuste automático de columnas
    worksheet.set_column('A:A', 28)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 25)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 25)
    worksheet.set_column('F:F', 10)
    worksheet.set_column('G:G', 17)

    workbook.close()
    return reporte_nombre


def enviar_correo(reporte_path, tipo_reporte, rango_fechas=None):
    # Día actual
    dia_actual = datetime.now().strftime("%d-%m-%Y")

    # Cargar las variables del archivo .env
    load_dotenv()
    name_account = os.getenv('SERVICE')
    from_address = os.getenv('FROM_ADDRESS')
    to_address = os.getenv('TO_ADDRESS')
    password_account = os.getenv('PASSWORD_ACCOUNT')
    subject = f'Reporte de Rendimientos Atención Ventanillas {tipo_reporte} del {dia_actual}.'
   
    # Descripción con la fecha
    if tipo_reporte == 'semanal' or tipo_reporte == 'mensual':
        body = f'Adjunto el {tipo_reporte} del rango de fechas: {rango_fechas}.Asociado con los rendimientos de los funcionarios en las ventanillas de atención al usuario.'
    else:
        body = f'Adjunto el reporte del día: {dia_actual}. Asociado con los rendimientos de los funcionarios en las ventanillas de atención al usuario.'
    
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar el archivo
    with open(reporte_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(reporte_path)}")
        msg.attach(part)

    # Enviar el correo
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(from_address, password_account)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()

    # Eliminar el archivo después de enviarlo
    os.remove(reporte_path)
    
if __name__ == "__main__":
    conn = conectar_db()
    if conn:
        # Reporte diario
        if datetime.now().weekday() < 5:  # Lunes a viernes
            turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo = obtener_indicadores_por_usuario(conn)
            reporte_path = generar_reporte(turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo, 'diario')
            enviar_correo(reporte_path, 'diario')

        # Reporte semanal
        if datetime.now().weekday() == 4:  # Viernes
            fecha_inicio_semana = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%d-%m-%Y")
            fecha_fin_semana = datetime.now().strftime("%d-%m-%Y")
            rango_fechas = f'{fecha_inicio_semana} a {fecha_fin_semana}'
            turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo = obtener_indicadores_por_usuario(conn)
            reporte_path = generar_reporte(turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo, 'semanal', rango_fechas)
            enviar_correo(reporte_path, 'semanal', rango_fechas)

        # Reporte mensual
        ultimo_dia_mes = (datetime.now() + timedelta(days=1)).month != datetime.now().month
        if ultimo_dia_mes:
            fecha_inicio_mes = datetime.now().replace(day=1).strftime("%d-%m-%Y")
            fecha_fin_mes = datetime.now().strftime("%d-%m-%Y")
            rango_fechas = f'{fecha_inicio_mes} a {fecha_fin_mes}'
            turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo = obtener_indicadores_por_usuario(conn)
            reporte_path = generar_reporte(turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo, 'mensual', rango_fechas)
            enviar_correo(reporte_path, 'mensual', rango_fechas)

        conn.close()