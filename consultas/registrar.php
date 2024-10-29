<?php
date_default_timezone_set('America/Bogota');
if (isset($_POST['registrar'])) {

	include('../funciones/conexion.php');
	require_once('../funciones/funciones.php');

	$respuesta = [];

	switch ($_POST['registrar']) {
		case 'reset-turnos':

			$fecha = date("Y-m-d H:i:s");
			$turno = "000";

			$sql = "DELETE FROM turnos;";
			$sql .= "ALTER TABLE turnos AUTO_INCREMENT=0";
			$error = "Error al resetear turno";

			$resetTurn = multi_consulta($con, $sql, $error);

			$sql = "DELETE FROM atencion;";
			$sql .= "ALTER TABLE atencion AUTO_INCREMENT=0";
			$error = "Error al resetear atencion";

			$resetAtention = multi_consulta($con, $sql, $error);

			if ($resetTurn == true && $resetAtention == true) {

				$respuesta = array('status' => 'correcto', 'mensaje' => 'Turnos reseteados correctamente', 'turno' => $turno);

			} else {

				$respuesta = array('status' => 'error', 'mensaje' => 'Error al resetear turnos', 'turno' => 000);

			}

			break;

		case 'turno':
			// Obtener el último turno
			$error = "Error al obtener turno";
			$sql = "SELECT turno FROM turnos ORDER BY id DESC LIMIT 1";
			$resultado = consulta($con, $sql, $error);
			$turno = "001";
			
			if ($resultado && mysqli_num_rows($resultado) > 0) {
				$ultimoTurno = mysqli_fetch_assoc($resultado);
				$turno = str_pad($ultimoTurno['turno'] + 1, 3, '0', STR_PAD_LEFT);
			}
			
			$fecha = date("Y-m-d H:i:s");
			
			// Asegurarse de recibir la cédula y el tipo de trámite
			if (isset($_POST['cedula']) && isset($_POST['tramite'])) {
				$cedula = $_POST['cedula'];
				$tramite = $_POST['tramite'];  // Se recibe el número (1, 2, 3 o 4)
			
				// Buscar el cliente en la base de datos
				$query = "SELECT id FROM clientes WHERE cedula = '$cedula'";
				$resultado2 = mysqli_query($con, $query);
			
				// Verificar si el cliente existe
				if ($resultado2 && mysqli_num_rows($resultado2) > 0) {
					// Si el cliente existe, obtener su id
					$cliente = mysqli_fetch_assoc($resultado2);
					$idCliente = $cliente['id'];
		
					// Insertar el turno con el número de trámite
					$query_turno = "INSERT INTO turnos (turno, idCliente, tramite, fechaRegistro) 
									VALUES ('$turno', '$idCliente', '$tramite', NOW())";
					mysqli_query($con, $query_turno);
			
					// Respuesta exitosa
					$respuesta = array('status' => 'success', 'message' => 'Turno registrado exitosamente', 'turno' => $turno);
				} else {
					// Si el cliente no existe, redireccionar al registro
					$respuesta = array('status' => 'error', 'message' => 'Cliente no encontrado, redireccionando a registro');
				}
			}
			break;


		case 'atencion':

			$idCaja = limpiar($con, $_POST['idCaja']);

			$registrar = false;

			$editar = false;

			$turno = '000';

			$error = "";

			$status = "";

			$mensaje = "";

			$ocupado = "";
			

			//funcion para dar un nuevo turno a la caja
			function darTurno($con, $idCaja)
			{

				$turno = '000';

				$sql = "select id,turno from turnos where atendido='0' order by id asc";
				$error = "Error al seleccionar el turno";

				$buscar = consulta($con, $sql, $error);

				$noResultados = mysqli_num_rows($buscar);

				//verificar si hay turnos disponibles
				if ($noResultados > 0) {

					$resultado = mysqli_fetch_assoc($buscar);
					$fecha = date("Y-m-d H:i:s");
					$turno = limpiar($con, $resultado['turno']);
					$idTurno = limpiar($con, $resultado['id']);
					if (isset($_POST['idUsuario'])) {
						$idUsuario = (int) $_POST['idUsuario']; // Convertir a entero
						error_log("ID Usuario recibido: " . $idUsuario); // Verifica en logs
					} else {
						$idUsuario = 1; // Valor predeterminado si no se recibe
						error_log("ID Usuario no recibido, valor por defecto: " . $idUsuario);
					}

					//poner el turno en la tabla de atenciones se agrega el turno idTurno en la tabla de Atencion
					$sql = "insert into atencion (turno,idCaja,idUsuario,fechaAtencion, idTurno) values ('$turno','$idCaja','$idUsuario','$fecha', '$idTurno')";
					$error = "Error al registrar el turno en atencion";
					$registrar = consulta($con, $sql, $error);

					//poner en la tabla turnos que caja lo esta atendiendo
					$sql = "update turnos set atendido='$idCaja' where turno='$turno'";
					$error = "Error al poner la caja que atiende el turno";
					$editar = consulta($con, $sql, $error);

					$nombre = "";
					$cedula = "";

					if ($registrar == true && $editar == true) {

						$status = "success";
						$mensaje = "Turno registrado";
						$ocupado = true;

						$sql = "select c.nombre, c.cedula from clientes c 
								inner join turnos t on c.id = t.idCliente 
								inner join atencion a on t.id = a.idTurno
							where a.idCaja = $idCaja and a.turno = '$turno' 
							order by a.id desc limit 1";
						$resultado_c = mysqli_query($con, $sql);
						if (mysqli_num_rows($resultado_c) > 0) {
							$cliente = mysqli_fetch_array($resultado_c);
							$nombre = $cliente["nombre"];
							$cedula = $cliente["cedula"];


						} else {
							$mensaje = "No se pudo cargar información del usuario a atender";
							$nombre = "";
							$cedula = "";
						}



					} else {

						$status = "error";
						$mensaje = "Error al dar los turnos" . $error;
						$ocupado = false;
						$nombre = "";
						$cedula = "";

					}

				} else {
    				// No hay turnos disponibles, se vacían los datos del cliente
					$status = "mensaje";
					$mensaje = "No hay turnos disponibles";
					$ocupado = false;
					$nombre="";
					$cedula="";

				}

				return array('turno' => $turno, 'status' => $status, 'mensaje' => $mensaje, 'ocupado' => $ocupado, 'nombre' => $nombre, 'cedula' => $cedula);

			}

			//funcion para consultar los turnos en la tabla atencion que no ha sido atendidos
			function turnosEnAtencion($con, $idCaja)
			{
				//seleccionar los turnos en la tabla atencion que correspondan a la caja y que estan en o en la columna atendido
				$sqlTurnosAtencion = "select id,turno from atencion where atendido='0' and idCaja='$idCaja'";

				$error = "Error al seleccionar el turno en atencion ";

				return $buscarTurnosAtencion = consulta($con, $sqlTurnosAtencion, $error);

			}

			//funcion para actualizar las atenciones de turnos
			function actualizarAtencion($con, $idCaja, $turno)
			{

				$sql = "update atencion set atendido='1' where turno='$turno' and idCaja='$idCaja'";

				$error = "Error al actualizar  el turno en atencion";

				$editar = consulta($con, $sql, $error);

			}

			//consultar los turnos en atencion
			$turnosAtencion = turnosEnAtencion($con, $idCaja);
			$noTurnosAtencion = mysqli_num_rows($turnosAtencion);

			if ($noTurnosAtencion == 0) {

				//dar un nuevo turno si no existen turnos sin atender 
				$resultado = darTurno($con, $idCaja);

				$turno = $resultado['turno'];
				$ocupado = $resultado['ocupado'];
				$status = $resultado['status'];
				$mensaje = $resultado['mensaje'];
				$nombre = $resultado['nombre'];
				$cedula = $resultado['cedula'];

			} else if ($noTurnosAtencion == 1) {

				//si solamente hay un turno por atender se actualiza la atencion y se da uno nuevo

				if ($_POST['turno'] != '000') {

					$turno = limpiar($con, $_POST['turno']);

				} else {

					$resultado = mysqli_fetch_assoc($turnosAtencion);

					$turno = $resultado['turno'];

				}

				actualizarAtencion($con, $idCaja, $turno);

				$resultado = darTurno($con, $idCaja);


				$turno = $resultado['turno'];

				$ocupado = $resultado['ocupado'];

				$status = $resultado['status'];

				$mensaje = $resultado['mensaje'];

				$nombre = $resultado['nombre'];
				$cedula = $resultado['cedula'];

			} else if ($noTurnosAtencion > 1) {

				//si hay mas de un turno se actualiza la atencion del turno que estaba siendo atendido y se envia el siguiente 
				$turno = limpiar($con, $_POST['turno']);

				actualizarAtencion($con, $idCaja, $turno);

				$turnosAtencion = turnosEnAtencion($con, $idCaja);

				$resultado = mysqli_fetch_assoc($turnosAtencion);

				$turno = $resultado['turno'];

				$ocupado = true;
				$status = "mensaje";
				$mensaje = "Existen turnos por atender";

			} else {

				$status = "error";

				$mensaje = "Error en la veririfaccion de turnos en atencion";

				$ocupado = false;


			}//veriricar que no haya mas turnos en atencion

			$respuesta = array(
				'status' => $status,
				'mensaje' => $mensaje,
				'turno' => $turno,
				'ocupado' => $ocupado,
				'idCaja' => $idCaja,
				'nombre' => $nombre,
				'cedula' => $cedula
			);
			break;

		default:

			$respuesta = array(
				'status' => 'error',
				'mensaje' => 'Peticion desconocida',
				'turno' => '000',
				'opcuado' => false,
				'idCaja' => '0',
				'nombre' => "",
				'cedula' => ""
			);

			break;

	}

	echo json_encode($respuesta);

} else {

	echo "<span>Opcion no valida</span>";

}
?>