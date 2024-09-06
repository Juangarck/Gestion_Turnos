<?php
include 'funciones/conexion.php';

$cedula = $_POST['cedula'];

$response = array();

if ($cedula) {
    $query = "SELECT * FROM clientes WHERE cedula = '$cedula'";
    $result = mysqli_query($conexion, $query);

    if ($result) {
        if (mysqli_num_rows($result) > 0) {
            $cliente = mysqli_fetch_assoc($result);
            $response['existe'] = true;
            $response['nombre'] = $cliente['nombre'];
            $response['telefono'] = $cliente['telefono'];
            // Agrega más campos según lo necesites
        } else {
            $response['existe'] = false;
            $response['message'] = 'Cliente no encontrado';
        }
    } else {
        $response['existe'] = false;
        $response['error'] = 'Error en la consulta a la base de datos';
    }
} else {
    $response['existe'] = false;
    $response['error'] = 'Cédula no proporcionada';
}

echo json_encode($response);
?>
