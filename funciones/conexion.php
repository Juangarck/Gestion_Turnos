<?php
	$host='localhost';
	$user='root';
	$password='';
	$db='turnero';
	$con=mysqli_connect($host,$user,$password,$db) or die ("<span class='mensaje'>Error al conectar con la base de datos</span>");
    // Establecer la codificación UTF-8 para la conexión
    mysqli_set_charset($con, "utf8");
?>