<?php

session_start();

if (isset($_SESSION['usuario']) && isset($_SESSION['password'])) {
	require_once('funciones/conexion.php');
	require_once('funciones/funciones.php');
	date_default_timezone_set('America/Bogota');

	?>

	<!doctype html>
	<html>

	<head>

		<meta charset="utf-8">

		<title>Caja <?php echo $_SESSION['idCaja']; ?></title>

		<link rel="stylesheet" type="text/css" href="css/generales.css">
		<link rel="stylesheet" type="text/css" href="css/caja.css">
		<link rel="stylesheet" type="text/css" href="css/sweetalert2.min.css">




	</head>

	<body>

		<div class="contenedor-principal">

			<div class="contenedor-caja">

				<?php

				$idCaja = $_SESSION['idCaja'];

				//seleccionar los turnos en la tabla atencion que correspondan a la caja y que estan en o en la columna atendido
				$sqlTurnosAtencion = "select id,turno from atencion where atendido='0' and idCaja='$idCaja'";
				$error = "Error al seleccionar el turno en atencion ";
				$buscarTurnosAtencion = consulta($con, $sqlTurnosAtencion, $error);

				$resultado = mysqli_fetch_assoc($buscarTurnosAtencion);
				$noResultados = mysqli_num_rows($buscarTurnosAtencion);

				if ($noResultados > 0) {

					$turno = $resultado['turno'];

				} else {

					$turno = "000";

				}

				?>

				<h1>Ventanilla <?php echo $_SESSION['idCaja']; ?></h1>

				<span class="datos-usuario">Funcionario: <?php echo $_SESSION['usuario']; ?></span>
				<span class="datos-turno">Turno: <span id="turno"><?php echo $turno; ?></span></span>
				<div class="datos-turno" id="cliente_atender"></div>


				<!--<input type="submit" name="atender" id="atender" value="Atender"> -->
				<button name="atender" id="atender">Atender</button>
				<input type="hidden" name="turno" id="noTurno" value="<?php echo $turno; ?>">
				<input type="hidden" id="idCaja" value="<?php echo $_SESSION['idCaja']; ?>">
				<input type="hidden" id="ocupado" value="false">

				<div class="contenedor-img-status"><img src="img/desconectado.png" id="imgStatus"></div>

				<a href="logout.php" class="salir" id="salir">Salir</a>

				<span id="mensajes"></span>

				<div>

				</div>
			</div>

		</div>
		<script src="js/jquery-3.1.0.min.js"></script>
		<script src="js/sweetalert2.all.min.js"></script>
		<script src="js/funcionesGenerales.js"></script>
		<script src="js/websocket.js"></script>

		<script src="js/caja.js"></script>
		

	</body>

	</html>

	<?php

} else {

	header('location:login.php');

}

?>