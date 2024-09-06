<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Solicitar turno</title>
    <link rel="stylesheet" type="text/css" href="css/generales.css">
    <link rel="stylesheet" type="text/css" href="css/solicitarTurno.css">
</head>
<body>
    <div class="contenedor-principal">
        <?php
            require_once('funciones/conexion.php');
            require_once('funciones/funciones.php');
            date_default_timezone_set('America/Bogota');
            
            // Obtener el último turno
            $sql = "SELECT turno FROM turnos ORDER BY id DESC LIMIT 1";
            $error = "Error al seleccionar el turno";
            $buscar = consulta($con,$sql,$error);
					
            $resultado = mysqli_fetch_assoc($buscar);	
            $noResultados = mysqli_num_rows($buscar);
            
            if($noResultados == 0){

                $turno = "000";

            }else{

                $turno = $resultado['turno'];

            }
            
            //datos de la empresa
            $sqlE = "SELECT * FROM info_empresa";
            $errorE = "Error al cargar datos de la empresa";
            $buscarE = consulta($con, $sqlE, $errorE);
            $info = mysqli_fetch_assoc($buscarE);
        ?>
        <div class="contenedor-caja">
            <header class="contenedor-logo">
                <figure class="logo-empresa">
                    <img src="<?php echo $info['logo']; ?>">
                </figure>
                <h1 class="nombre-empresa"><?php echo $info['nombre']; ?> Bienvenido Apreciado Usuario</h1>
            </header>
            <div class="clear"></div>
            <span class="datos-turno">Último Turno: <span id="turno"><?php echo $turno; ?></span></span>
                <form id="formCedula" method="POST" action="verificar_cedula.php">
                    <label for="cedula">Ingrese su cédula de ciudadanía:</label>
                    <input type="text" id="cedula" name="cedula" required>
                    <button type="submit">Verificar</button>
                </form>
        </div>
    </div>
    <script src="js/jquery-3.1.0.min.js"></script>
    <script src="js/funcionesGenerales.js"></script>
    <script src="js/solicitarTurno.js"></script>
</body>
</html>

<?php
include 'funciones/conexion.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $cedula = $_POST['cedula'];

    // Consulta para verificar si la cédula existe
    $stmt = $conn->prepare("SELECT * FROM clientes WHERE cedula = ?");
    $stmt->bind_param("s", $cedula);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows > 0) {
        // Cliente existe, obtenemos el id
        $cliente = $result->fetch_assoc();
        $cliente_id = $cliente['id'];
    } else {
        // Registrar nuevo cliente
        $nombre = $_POST['nombre'];
        $telefono = $_POST['telefono'];
        $email = $_POST['email'];
        $direccion = $_POST['direccion'];

        $sql = "INSERT INTO clientes (nombre, cedula, telefono, email, direccion) VALUES (?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("sssss", $nombre, $cedula, $telefono, $email, $direccion);
        $stmt->execute();
        $cliente_id = $stmt->insert_id;
    }

    // Obtener el último turno generado
    $sql = "SELECT turno FROM turnos ORDER BY id DESC LIMIT 1";
    $result = $conn->query($sql);
    $row = $result->fetch_assoc();
    $ultimo_turno = isset($row['turno']) ? $row['turno'] : 0; // Si no hay turnos, empieza en 0

    // Generar el nuevo turno de manera secuencial
    $nuevo_turno = $ultimo_turno + 1;

    // Registrar el turno
    $sql = "INSERT INTO turnos (turno, cliente_id) VALUES (?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("si", $nuevo_turno, $cliente_id);
    $stmt->execute();

    echo "Turno solicitado: " . $nuevo_turno;
}
?>
