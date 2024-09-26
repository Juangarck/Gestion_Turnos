<?php
include 'funciones/conexion.php';  // Esto incluirá la variable $con
session_start();  // Asegúrate de que la sesión esté iniciada

if (isset($_POST['cedula'])) {
    $cedula = $_POST['cedula'];

    // Preparar una consulta SQL segura
    $stmt = $con->prepare("SELECT * FROM clientes WHERE cedula = ?");
    $stmt->bind_param("s", $cedula);  // La "s" indica que es un string
    $stmt->execute();
    $result = $stmt->get_result();

    if($result->num_rows > 0) {
        $cliente = $result->fetch_assoc();
        // Redirigir a la página de turno con el nombre del cliente y su número de turno
        // header("Location: solicitar_turno.php?cedula={$cliente['cedula']}");
        
        //aca envio la cedula para que sea recibio por la funcion ajax verificar
        echo json_encode(array('respuesta' => true, 'cedula' => $cliente['cedula'], 'nombre' => $cliente['nombre']));

    } else {
        // Redirigir a la página de registro si no existe
        // header("Location: registro.php");
        $_SESSION['cedula'] = $cedula;
        echo json_encode(array('respuesta'=>false));
    }

    $stmt->close();  // Cerrar la declaración
}
?>
