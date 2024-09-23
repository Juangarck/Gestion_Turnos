<?php
include './funciones/conexion.php'; 
include './funciones/funciones.php';
date_default_timezone_set('America/Bogota');

$errores = [];
$exito = false; 

$nombre = $cedula = $telefono = $email = $direccion = $municipio= '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = limpiar($con, trim($_POST['nombre']));
    $cedula = limpiar($con, trim($_POST['cedula']));
    $telefono = limpiar($con, trim($_POST['telefono']));
    $email = limpiar($con, trim($_POST['email']));
    $municipio = limpiar($con, trim($_POST['municipio']));
    $direccion = limpiar($con, trim($_POST['direccion']));
    $fechaRegistro = date('Y-m-d H:i:s');
    $autorizacion = isset($_POST['autorizacion']) ? $_POST['autorizacion'] : '';

    if (empty($nombre)) {
        $errores[] = "El nombre es obligatorio.";
    }

    if (empty($cedula)) {
        $errores[] = "La cédula es obligatoria.";
    }

    if (empty($telefono)) {
        $errores[] = "El número de celular es obligatorio.";
    }

    if (!preg_match("/^[0-9]{5,20}$/", $cedula)) {
        $errores[] = "El formato de la cédula es incorrecto.";
    }

    if (!preg_match("/^[0-9]{4,20}$/", $telefono)) {
        $errores[] = "El formato del teléfono es incorrecto.";
    }

    if (!empty($email) && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errores[] = "El formato del correo electrónico es inválido.";
    }

    if (empty($autorizacion)) {
        $errores[] = "Debe aceptar la autorización para el uso de sus datos personales.";
    }

    if (empty($errores)) {
        $autorizacion = 1;
        $query = "INSERT INTO clientes (nombre, cedula, telefono, email, municipio, direccion, fechaRegistro, autorizacion) 
                  VALUES ('$nombre', '$cedula', '$telefono', '$email', '$municipio', '$direccion', '$fechaRegistro', '$autorizacion')";
        $result = consulta($con, $query, "Error al registrar el usuario.");

        if ($result) {
            $exito = true;
        } else {
            $errores[] = "Error al registrar el usuario. Por favor, intente nuevamente.";
        }
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro de Usuario</title>
    <link rel="stylesheet" href="css/styles_registro_clientes.css">
</head>
<body>
    <div class="container">
        <h1>Registro de Usuario</h1>
        <?php if (!empty($errores)): ?>
            <div class="error">
                <ul>
                    <?php foreach ($errores as $error): ?>
                        <li><?php echo $error; ?></li>
                    <?php endforeach; ?>
                </ul>
            </div>
        <?php endif; ?>
        
        <?php if ($exito): ?>
            <div>
                <p>¡Registro exitoso! Su cédula es <?php echo htmlspecialchars($cedula); ?>.</p>
                <p>Apreciado Usuario, ya se completó su registro, AHORA, <strong>NO OLVIDE SOLICITAR SU TURNO</strong>.</p>
                <a href="solicitar_turno.php">Volver a la página principal</a>
            </div>
        <?php else: ?>
            <form method="POST" action="registro.php" autocomplete="off">
                <label for="nombre">Nombres y apellidos:</label>
                <input type="text" id="nombre" name="nombre" value="<?php echo htmlspecialchars($nombre); ?>" required>

                <label for="cedula">Cédula:</label>
                <input type="text" id="cedula" name="cedula" value="<?php echo htmlspecialchars($cedula); ?>" required>

                <label for="telefono">Celular:</label>
                <input type="text" id="telefono" name="telefono" value="<?php echo htmlspecialchars($telefono); ?>" required>

                <label for="email">Correo Electrónico:</label>
                <input type="email" id="email" name="email" value="<?php echo htmlspecialchars($email); ?>">

                <label for="municipio">Municipio de Residencia:</label>
                <input type="text" id="municipio" name="municipio" value="<?php echo htmlspecialchars($municipio); ?>">

                <label for="direccion">Dirección:</label>
                <textarea id="direccion" name="direccion"><?php echo htmlspecialchars($direccion); ?></textarea>

                <div class="autorizacion">
                    <label>
                        <input type="checkbox" name="autorizacion" value="1" required>
                        Autorizo el tratamiento de mis datos personales de acuerdo con la Ley 1581 de 2012 y el Decreto 1377 de 2013. Los datos serán utilizados únicamente para los fines establecidos en la política de privacidad.
                    </label>
                </div>

                <button type="submit">Registrar</button>
            </form>
        <?php endif; ?>
    </div>
</body>
</html>

