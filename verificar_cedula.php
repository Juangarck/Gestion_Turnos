<?php
include 'funciones/conexion.php';

$cedula = $_POST['cedula'];
$query = "SELECT * FROM clientes WHERE cedula = '$cedula'";
$result = mysqli_query($conexion, $query);

if(mysqli_num_rows($result) > 0) {
    $cliente = mysqli_fetch_assoc($result);
    // Redirigir a la página de turno con el nombre del cliente y su número de turno
    header("Location: turno.php?nombre={$cliente['nombre']}&cedula={$cliente['cedula']}");
} else {
    // Redirigir a la página de registro si no existe
    header("Location: registro.php");
}
?>
