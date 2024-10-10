<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Solicitar turno</title>
    <link rel="stylesheet" type="text/css" href="css/generales.css">
    <link rel="stylesheet" type="text/css" href="css/solicitarTurno.css">
    <link rel="stylesheet" type="text/css" href="css/sweetalert2.min.css">
</head>
<body>
    <div class="contenedor-principal">
        <?php
            require_once('funciones/conexion.php');
            require_once('funciones/funciones.php');
            date_default_timezone_set('America/Bogota');
            
            // Obtener el último turno
            $sql = "SELECT turno, idCliente FROM turnos ORDER BY id DESC LIMIT 1";
            $error = "Error al seleccionar el turno";
            $buscar = consulta($con,$sql,$error);
					
            $resultado = mysqli_fetch_assoc($buscar);	
            $noResultados = mysqli_num_rows($buscar);

            // definimos los posibles tipos de tramites y su equivalencia
            $tramites = [
                "1" => "Productos catastrales",
                "2" => "Trámites catastrales",
                "3" => "Peticiones, quejas o reclamos",
                "4" => "Consultas u orientación"
            ];

            if($noResultados == 0){

                $turno = "000";
                $idCliente ="0";

            }else{

                $turno = $resultado['turno'];
                $idCliente = $resultado['idCliente'];

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
                <form id="formCedula" method="POST" autocomplete="off">
                    <label for="cedula">Ingrese su cédula de ciudadanía:</label>
                    <input type="text" id="cedula" name="cedula" required>
                    
                    <label for="tramite">Seleccione el tipo de trámite requerido</label>
                    <select id="tramite" name="tramite"required>
                        <option value="" disabled selected hidden>Seleccione el tipo de trámite</option> <!-- Opción inválida -->
                        <?php
                        foreach ($tramites as $clave => $nombre) {
                            echo "<option value='$clave'>$nombre</option>";
                        }
                        ?>
                    </select>
                    
                    <button type="submit" id="verificar" class="btn">Verificar</button>
                </form>
        </div>

            <div>
                
            </div>

    </div>
    <script src="js/jquery-3.1.0.min.js"></script>
    <script src="js/sweetalert2.all.min.js"></script>   
    <script src="js/funcionesGenerales.js"></script>
    <script src="js/solicitarTurno.js"></script>
    
</body>
</html>

