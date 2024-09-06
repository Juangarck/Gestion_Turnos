<?php
include 'funciones/conexion.php'; // Incluye el archivo de conexión
include '/funciones/funciones.php';
date_default_timezone_set('America/Bogota');

$errores = [];
$exito = false;  // Variable para controlar si el registro fue exitoso

// Definir variables para evitar errores "undefined"
$nombre = $cedula = $telefono = $email = $direccion = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Escapando y limpiando entradas de usuario
    $nombre = limpiar($con, trim($_POST['nombre']));
    $cedula = limpiar($con, trim($_POST['cedula']));
    $telefono = limpiar($con, trim($_POST['telefono']));
    $email = limpiar($con, trim($_POST['email']));
    $direccion = limpiar($con, trim($_POST['direccion']));
    $fechaRegistro = date('Y-m-d H:i:s');

    // Validar que los campos obligatorios no estén vacíos
    if (empty($nombre)) {
        $errores[] = "El nombre es obligatorio.";
    }

    if (empty($cedula)) {
        $errores[] = "La cédula es obligatoria.";
    }
    if (empty($telefono)) {
        $error[] = "El telefono es obligatorio.";
    }

    // Validar formato de cédula
    if (!preg_match("/^[0-9]{5,20}$/", $cedula)) {
        $errores[] = "El formato de la cédula es incorrecto.";
    }

    // Validar formato de correo electrónico si se ha ingresado
    if (!empty($email) && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errores[] = "El formato del correo electrónico es inválido.";
    }

    // Si no hay errores, proceder con la inserción en la base de datos
    if (empty($errores)) {
        $query = "INSERT INTO clientes (nombre, cedula, telefono, email, direccion, fechaRegistro) 
                  VALUES ('$nombre', '$cedula', '$telefono', '$email', '$direccion', '$fechaRegistro')";
        $result = consulta($con, $query, "Error al registrar el usuario.");

        if ($result) {
            $exito = true;  // Indicar que el registro fue exitoso
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
    <link rel="stylesheet" href="css/styles_registro_clientes.css"> <!-- Aquí se referencia el archivo CSS -->
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
                <a href="solicitar_turno.php">Volver a la página principal</a>
            </div>
        <?php else: ?>
            <form method="POST" action="registro.php">
                <label for="nombre">Nombre:</label>
                <input type="text" id="nombre" name="nombre" value="<?php echo htmlspecialchars($nombre); ?>" required>

                <label for="cedula">Cédula:</label>
                <input type="text" id="cedula" name="cedula" value="<?php echo htmlspecialchars($cedula); ?>" required>

                <label for="telefono">Teléfono:</label>
                <input type="text" id="telefono" name="telefono" value="<?php echo htmlspecialchars($telefono); ?>">

                <label for="email">Correo Electrónico:</label>
                <input type="email" id="email" name="email" value="<?php echo htmlspecialchars($email); ?>">

                <label for="direccion">Dirección:</label>
                <textarea id="direccion" name="direccion"><?php echo htmlspecialchars($direccion); ?></textarea>
                
                <button type="submit">Registrar</button>
            </form>
        <?php endif; ?>
    </div>
</body>
</html>
