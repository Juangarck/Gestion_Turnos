<?php
// Obtener los parámetros de la solicitud POST
$turno = $_POST['turno'];
$ventanilla = $_POST['ventanilla'];
$cliente = $_POST['cliente'];

// Asegurarse de que los parámetros estén definidos
if (isset($turno) && isset($ventanilla) && isset($cliente)) {
    // Crear el comando para ejecutar el script Python con los parámetros
    $scriptPath = realpath('C:\xampp\htdocs\turnero\llamado_voz.py'); // Obtener la ruta absoluta del script Python
    $command = escapeshellcmd("python3 $scriptPath $turno $ventanilla '$cliente'");

    
    // Ejecutar el comando
    shell_exec($command);
    
    // Devolver una respuesta de éxito
    echo json_encode(["status" => "success", "message" => "Turno llamado exitosamente"]);
} else {
    echo json_encode(["status" => "error", "message" => "Faltan parámetros"]);
}
?>