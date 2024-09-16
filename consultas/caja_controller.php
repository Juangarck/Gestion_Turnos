<?php
include('../funciones/conexion.php');
require_once('../funciones/funciones.php');

//codigo que permite ver que cliente se va atender en la caja


$idCaja = $_POST['idCaja'];
$turno = $_POST['turno'];
$sql = "select c.nombre, c.cedula from clientes c 
    inner join turnos t on c.id = t.idCliente 
    inner join atencion a on t.id = a.idTurno
   where a.idCaja = $idCaja and a.turno = '$turno' 
   order by a.id desc limit 1";
$resultado = mysqli_query($con, $sql);
if (mysqli_num_rows($resultado) > 0) {
    $cliente = mysqli_fetch_array($resultado);
    $nombre = $cliente["nombre"];
    $cedula = $cliente["cedula"];

    $respuesta = json_encode(array("status" => "success", "nombre" => $nombre, "cedula" => $cedula));
    echo $respuesta;

} else {
    echo json_encode(array("status" => "error", "nombre" => "", "cedula" => ""));
}


?>