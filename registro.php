<?php
include './funciones/conexion.php'; 
include './funciones/funciones.php';
date_default_timezone_set('America/Bogota');

session_start(); // Iniciar sesión

$errores = [];
$exito = false; 

$nombre = $cedula = $telefono = $email = $direccion = $municipio = '';

// Precargar el símbolo @ en el correo electrónico
$email = '@';

// Si ya hay una cédula en la sesión, usarla para precargar el formulario
if (isset($_SESSION['cedula'])) {
    $cedula = $_SESSION['cedula'];
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = limpiar($con, trim($_POST['nombre']));
    $cedula = limpiar($con, trim($_POST['cedula']));
    $telefono = limpiar($con, trim($_POST['telefono']));
    $email = limpiar($con, trim($_POST['email']));
    $municipio = limpiar($con, trim($_POST['municipio']));
    $direccion = limpiar($con, trim($_POST['direccion']));
    $fechaRegistro = date('Y-m-d H:i:s');
    $autorizacion = isset($_POST['autorizacion']) ? $_POST['autorizacion'] : '';

    // Guardar la cédula en la sesión para precargarla si hay errores
    $_SESSION['cedula'] = $cedula;

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

    // Validar si el campo email contiene solo '@' o está vacío
    if (trim($email) === '@') {
        $email = '';  // Considerar como campo vacío
    } elseif (!empty($email) && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errores[] = "El formato del correo electrónico es inválido.";
    }

    if (empty($autorizacion)) {
        $errores[] = "Debe aceptar la autorización para el uso de sus datos personales.";
    }

    if (empty($errores)) {
        $autorizacion = 1;
        // Convertir el nombre a mayúsculas antes de guardarlo
        $nombre = strtoupper($nombre);        
        $query = "INSERT INTO clientes (nombre, cedula, telefono, email, municipio, direccion, fechaRegistro, autorizacion) 
                  VALUES ('$nombre', '$cedula', '$telefono', '$email', '$municipio', '$direccion', '$fechaRegistro', '$autorizacion')";
        $result = consulta($con, $query, "Error al registrar el usuario.");

        if ($result) {
            // Borrar la cédula de la sesión una vez el registro sea exitoso
            unset($_SESSION['cedula']);
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
                <label for="nombre">Nombres y apellidos: <span class="required">*</span></label>
                <input type="text" id="nombre" name="nombre" value="<?php echo htmlspecialchars($nombre); ?>" required>

                <label for="cedula">Cédula: <span class="required">*</span></label>
                <input type="text" id="cedula" name="cedula" value="<?php echo htmlspecialchars($cedula); ?>" required>

                <label for="telefono">Celular: <span class="required">*</span></label>
                <input type="text" id="telefono" name="telefono" value="<?php echo htmlspecialchars($telefono); ?>" required>

                <label for="email">Correo Electrónico:</label>
                <!-- Cambiar el tipo a text -->
                <input type="text" id="email" name="email" value="<?php echo htmlspecialchars($email); ?>" placeholder="usuario@dominio.com">

                <label for="municipio">Municipio de Residencia:</label>
                <input type="text" id="municipio" name="municipio" value="<?php echo htmlspecialchars($municipio); ?>">

                <label for="direccion">Dirección:</label>
                <textarea id="direccion" name="direccion"><?php echo htmlspecialchars($direccion); ?></textarea>

                <div class="autorizacion">
                    <label>
                        <input type="checkbox" name="autorizacion" value="1" required>
                        Autorizo el tratamiento de mis datos personales de acuerdo con la Ley 1581 de 2012 y el Decreto 1377 de 2013. Los datos serán utilizados únicamente para los fines establecidos en la política de privacidad. <span class="required">*</span>
                    </label>
                </div>

                <button type="submit">Registrar</button>
            </form>
        <?php endif; ?>
    </div>

    <script>
    document.querySelector('form').addEventListener('submit', function(event) {
        var emailField = document.getElementById('email');
        var emailValue = emailField.value.trim();

        // Validar el campo de correo electrónico
        if (emailValue === '@') {
            emailField.value = ''; // Limpiar el campo si solo contiene '@'
        } else if (emailValue !== '' && !/^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/.test(emailValue)) {
            event.preventDefault(); // Detener el envío del formulario
            alert('Por favor, introduce una dirección de correo válida o deja el campo vacío.');
        }
    });
    </script>
</body>
</html>

