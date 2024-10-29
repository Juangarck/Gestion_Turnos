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

# Función para obtener el rango de fechas
def obtener_rango_fechas(tipo_reporte):
    hoy = datetime.now()

    if tipo_reporte == 'diario':
        # Para diario solo usamos el día actual
        fecha_inicio = fecha_fin = hoy.strftime("%Y-%m-%d")
    elif tipo_reporte == 'semanal':
        # Para semanal, obtener desde el lunes de esta semana hasta el viernes
        inicio_semana = hoy - timedelta(days=hoy.weekday())  # lunes
        fin_semana = inicio_semana + timedelta(days=4)  # viernes
        fecha_inicio = inicio_semana.strftime("%Y-%m-%d")
        fecha_fin = fin_semana.strftime("%Y-%m-%d")
    elif tipo_reporte == 'mensual':
        # Para mensual, obtener desde el primer día hasta el último día del mes
        fecha_inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
        fecha_fin = (hoy.replace(month=hoy.month + 1, day=1) - timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        raise ValueError("Tipo de reporte no válido")

    return fecha_inicio, fecha_fin

# Actualizar las consultas para filtrar por rango de fechas
def obtener_indicadores_por_usuario(conn, tipo_reporte):
    cursor = conn.cursor()
    
    # Obtener el rango de fechas basado en el tipo de reporte
    fecha_inicio, fecha_fin = obtener_rango_fechas(tipo_reporte)
    
    # 1. Turnos atendidos por FUNCIONARIO en el rango de fechas correspondiente DIA / SEMANA / MES
    query_turnos = """
    SELECT a.idUsuario, u.usuario, DATE(fechaAtencion) as fecha, COUNT(*) as turnos_atendidos
    FROM atencion a
    JOIN usuarios u ON a.idUsuario = u.id
    WHERE DATE(fechaAtencion) BETWEEN %s AND %s
    GROUP BY idUsuario, DATE(fechaAtencion)
    """
    cursor.execute(query_turnos, (fecha_inicio, fecha_fin))
    turnos = cursor.fetchall()

    # 2. Tiempo promedio de espera de los clientes por funcionario en el rango de fechas DIA / SEMANA / MES
    query_tiempo = """
    (SELECT a.idUsuario, AVG(TIMESTAMPDIFF(MINUTE, t.fechaRegistro, a.fechaAtencion)) as tiempo_promedio
    FROM atencion a
    JOIN turnos t ON a.turno = t.turno
    WHERE DATE(a.fechaAtencion) BETWEEN %s AND %s
    GROUP BY a.idUsuario)

    UNION ALL

    (SELECT 'GLOBAL' as idUsuario, AVG(TIMESTAMPDIFF(MINUTE, t.fechaRegistro, a.fechaAtencion)) as tiempo_promedio
    FROM atencion a
    JOIN turnos t ON a.turno = t.turno
    WHERE DATE(a.fechaAtencion) BETWEEN %s AND %s)
    """
    cursor.execute(query_tiempo, (fecha_inicio, fecha_fin, fecha_inicio, fecha_fin))
    tiempos = cursor.fetchall()
    
    # 3. Hora (UNA) de mayor atención de turnos por FUNCIONARIO en el rango de fechas
    query_hora_por_cajera = """
        SELECT a.idUsuario, u.usuario, HOUR(a.fechaAtencion) AS hora, COUNT(*) AS turnos_atendidos
        FROM atencion a
        JOIN usuarios u ON a.idUsuario = u.id
        WHERE DATE(a.fechaAtencion) BETWEEN %s AND %s
        GROUP BY a.idUsuario, u.usuario, HOUR(a.fechaAtencion)
        HAVING turnos_atendidos = (
            SELECT MAX(turnos_atendidos)
            FROM (
                SELECT a2.idUsuario, HOUR(a2.fechaAtencion) AS hora, COUNT(*) AS turnos_atendidos
                FROM atencion a2
                WHERE DATE(a2.fechaAtencion) BETWEEN %s AND %s
                GROUP BY a2.idUsuario, HOUR(a2.fechaAtencion)
            ) AS max_turnos
            WHERE max_turnos.idUsuario = a.idUsuario
        )
        ORDER BY a.idUsuario;
    """

    cursor.execute(query_hora_por_cajera, (fecha_inicio, fecha_fin, fecha_inicio, fecha_fin))
    hora_pico_por_cajera = cursor.fetchall()


    # 4. Hora de mayor atención a nivel global en el rango de fechas
    query_hora_global = """
    SELECT HOUR(a.fechaAtencion) as hora, COUNT(*) as turnos_atendidos
    FROM atencion a
    WHERE DATE(a.fechaAtencion) BETWEEN %s AND %s
    GROUP BY HOUR(a.fechaAtencion)
    ORDER BY turnos_atendidos DESC
    LIMIT 1
    """
    cursor.execute(query_hora_global, (fecha_inicio, fecha_fin))
    hora_pico_global = cursor.fetchone()

    # 5. Cantidad total de clientes atendidos y tiempo promedio de espera en el rango de fechas
    query_total_clientes_y_tiempo = """
    SELECT COUNT(*) as total_clientes,
        AVG(TIMESTAMPDIFF(MINUTE, t.fechaRegistro, a.fechaAtencion)) as tiempo_promedio_espera
    FROM atencion a
    JOIN turnos t ON a.turno = t.turno
    WHERE DATE(a.fechaAtencion) BETWEEN %s AND %s
    """
    cursor.execute(query_total_clientes_y_tiempo, (fecha_inicio, fecha_fin))
    total_clientes_tiempo = cursor.fetchone()

    return turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo

def obtener_tramites(conn, tipo_reporte):
    cursor = conn.cursor()

    # Obtener el rango de fechas basado en el tipo de reporte
    fecha_inicio, fecha_fin = obtener_rango_fechas(tipo_reporte)

    query_tramites = """
    SELECT tramite, COUNT(*) as cantidad
    FROM turnos
    WHERE DATE(fechaRegistro) BETWEEN %s AND %s
    GROUP BY tramite
    """
    cursor.execute(query_tramites, (fecha_inicio, fecha_fin))
    tramites = cursor.fetchall()
    
    # Diccionario de equivalencias
    tramites_dict = {
        "1": "Productos catastrales",
        "2": "Trámites catastrales",
        "3": "Peticiones, quejas o reclamos",
        "4": "Consultas u orientación"
    }
    
    # Crear lista de tuplas con la descripción del trámite y la cantidad
    tramites_con_descripcion = [(tramites_dict[str(tramite[0])], tramite[1]) for tramite in tramites]
    
    return tramites_con_descripcion

def generar_reporte(turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo, tipo_reporte, tramites_con_descripcion, rango_fechas=None):
    fecha_inicio, fecha_fin = obtener_rango_fechas(tipo_reporte)
    rango_fechas = f"{fecha_inicio} al {fecha_fin}" if tipo_reporte != 'diario' else None
    
    reporte_nombre = f'reporte_turnos_{tipo_reporte}.xlsx'
    workbook = xlsxwriter.Workbook(reporte_nombre)
    worksheet = workbook.add_worksheet()

    formato_bold_centrado = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
    formato_centrado = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    formato_bordes = workbook.add_format({'border': 1})
    
    # Obtiene la ruta actual donde se ejecuta el script
    script_path = os.path.dirname(os.path.abspath(__file__))

    # Navega una carpeta hacia atrás y luego hacia la subcarpeta 'img'
    image_path = os.path.join(script_path, '..', 'img', '49550310_598832710562102_5995102219237874750_n.jpg')

    # Normaliza la ruta (para evitar problemas con diferentes sistemas operativos)
    imagen_path = os.path.normpath(image_path)

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
            # Si el reporte es diario, escribir solo la fecha del turno
            if tipo_reporte == 'diario':
                worksheet.write(row, 2, str(turno[2]))  # Fecha de turno (día actual)
            # Si es semanal o mensual, usar el rango de fechas proporcionado
            else:
                worksheet.write(row, 2, str(rango_fechas))  # Rango de fechas (p.ej. "09-09-2024 al 13-09-2024")
            worksheet.write(row, 3, turno[3])
            row += 1

    if tiempos:
        row = 3
        for tiempo in tiempos:
            if tiempo[1] is not None:
                worksheet.write(row, 4, float(tiempo[1]))
            else:
                worksheet.write(row, 4, 'N/A')  # O el valor predeterminado que prefieras
            row += 1

    if hora_pico_por_cajera:
        row = 3
        for hora in hora_pico_por_cajera:
            worksheet.write(row, 5, hora[2])
            worksheet.write(row, 6, hora[3])
            row += 1

    row += 2
    # En la parte de generar_reporte, antes de acceder a hora_pico_global[0] y hora_pico_global[1]
    if hora_pico_global:
        worksheet.write(row, 0, 'Hora Pico Global')
        worksheet.write(row, 1, hora_pico_global[0])
        worksheet.write(row + 1, 0, 'Turnos en Hora Pico Global')
        worksheet.write(row + 1, 1, hora_pico_global[1])
    else:
        worksheet.write(row, 0, 'Hora Pico Global')
        worksheet.write(row, 1, 'N/A')  # O algún valor por defecto
        worksheet.write(row + 1, 0, 'Turnos en Hora Pico Global')
        worksheet.write(row + 1, 1, 'N/A')  # O algún valor por defecto

    worksheet.write(row + 3, 0, 'Total Clientes Atendidos')
    worksheet.write(row + 3, 1, total_clientes_tiempo[0])
    worksheet.write(row + 4, 0, 'Tiempo Promedio de Espera (min)')
    worksheet.write(row + 4, 1, total_clientes_tiempo[1])

    # Agregar el conteo de trámites al final del reporte
    row += 6
    worksheet.write(row, 0, 'Conteo de trámites', formato_bold_centrado)
    row += 1
    worksheet.write(row, 0, 'Trámite')
    worksheet.write(row, 1, 'Cantidad')

    for tramite in tramites_con_descripcion:
        row += 1
        worksheet.write(row, 0, tramite[0])  # Descripción del trámite
        worksheet.write(row, 1, tramite[1])  # Cantidad de turnos

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
    
    # Descripción con la fecha del ASUNTO
    if tipo_reporte == 'semanal' or tipo_reporte == 'mensual':
        subject = f'Reporte de Rendimientos Atención Ventanillas del rango de fechas: {rango_fechas}'
    else:
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

    # Enviar el correo
    try:
        server.sendmail(from_address, to_address, msg.as_string())
        # Eliminar el archivo después de enviarlo
        os.remove(reporte_path)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    server.quit()
    
if __name__ == "__main__":
    conn = conectar_db()
    if conn:
        # Reporte diario
        if datetime.now().weekday() < 5:  # Lunes a viernes
            turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo = obtener_indicadores_por_usuario(conn, 'diario')
            tramites_con_descripcion = obtener_tramites(conn, 'diario')  # Obtener los trámites
            reporte_path = generar_reporte(turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo, 'diario', tramites_con_descripcion)  # Pasar trámites como argumento
            enviar_correo(reporte_path, 'diario')

        # Reporte semanal
        if datetime.now().weekday() == 4:  # Viernes
            fecha_inicio_semana = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%d-%m-%Y")
            fecha_fin_semana = datetime.now().strftime("%d-%m-%Y")
            rango_fechas = f'{fecha_inicio_semana} a {fecha_fin_semana}'
            turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo = obtener_indicadores_por_usuario(conn, 'semanal')
            tramites_con_descripcion = obtener_tramites(conn, 'semanal')  # Obtener los trámites
            reporte_path = generar_reporte(turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo, 'semanal', tramites_con_descripcion, rango_fechas)  # Pasar trámites como argumento
            enviar_correo(reporte_path, 'semanal', rango_fechas)

        # Reporte mensual
        ultimo_dia_mes = (datetime.now() + timedelta(days=1)).month != datetime.now().month
        if ultimo_dia_mes:
            fecha_inicio_mes = datetime.now().replace(day=1).strftime("%d-%m-%Y")
            fecha_fin_mes = datetime.now().strftime("%d-%m-%Y")
            rango_fechas = f'{fecha_inicio_mes} a {fecha_fin_mes}'
            turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo = obtener_indicadores_por_usuario(conn, 'mensual')
            tramites_con_descripcion = obtener_tramites(conn, 'mensual')  # Obtener los trámites
            reporte_path = generar_reporte(turnos, tiempos, hora_pico_por_cajera, hora_pico_global, total_clientes_tiempo, 'mensual', tramites_con_descripcion, rango_fechas)  # Pasar trámites como argumento
            enviar_correo(reporte_path, 'mensual', rango_fechas)

        conn.close()