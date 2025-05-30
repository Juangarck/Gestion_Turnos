﻿﻿<!doctype html>
<html>

<head>

    <meta charset="utf-8">

    <title>Turnos</title>

    <link rel="stylesheet" type="text/css" href="css/generales.css">
    <link rel="stylesheet" type="text/css" href="css/responsivo-turnos.css">
    <link rel="stylesheet" type="text/css" href="css/turnos.css">


</head>

<body>

    <div class="contenedor-principal">


        <?php

        require_once('funciones/conexion.php');
        require_once('funciones/funciones.php');
        date_default_timezone_set('America/Bogota');

        //datos de la empresa
        $sql = "select * from info_empresa";
        $error = "Error al cargar datos de la empresa ";
        $search = consulta($con, $sql, $error);

        $info = mysqli_fetch_assoc($search);


        //turno atendido
        $sqlTA = "select a.turno, a.idCaja, c.nombre from atencion a 
                 inner join turnos t on t.id = a.idTurno
                inner join clientes c on t.idCliente = c.id
                order by t.id desc";
        $errorTA = "Error al cargar el turno atendido";
        $searchTA = consulta($con, $sqlTA, $errorTA);

        if (mysqli_num_rows($searchTA) > 0) {

            $turno = mysqli_fetch_assoc($searchTA);
            $numeroTurno = $turno['turno'];
            $caja = $turno['idCaja'];
            $nombreCompleto = ucwords(strtolower($turno['nombre']));
            $nombreArray = explode(' ', $nombreCompleto);
            $primerNombre = $nombreArray[0];
            $primerApellido = isset($nombreArray[2]) ? $nombreArray[2][0] : (isset($nombreArray[1]) ? $nombreArray[1][0] : '');
            $nombreFormateado = $primerNombre . ' ' . $primerApellido;
            $cliente = $nombreFormateado;

        } else {

            $numeroTurno = '000';
            $caja = '0';

        }

        // Enviar los datos por POST para generar el audio
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $num_turno = isset($_POST['numeroTurno']) ? htmlspecialchars($_POST['numeroTurno']) : $numeroTurno;
            $num_ventanilla = isset($_POST['caja']) ? htmlspecialchars($_POST['caja']) : $caja;
            $nom_cliente = isset($_POST['nombreCompleto']) ? htmlspecialchars($_POST['nombreCompleto']) : $nombreCompleto;

            // Ejecutar el script de Python para la generación de audio
            $command = escapeshellcmd("py llamado_voz.py $num_turno $num_ventanilla '$nom_cliente'");
            #$command = escapeshellcmd("py llamado_voz.py 25 5 'Juan F'");
            $output = shell_exec($command);
            echo $output;

            // El archivo de audio generado se llamará turno_$num_turno.ogg
            $audio_file = "tonos/turno_" . $num_turno . ".ogg"; // ruta del archivo generado

            // Devolver respuesta al cliente
            echo json_encode([
                'status' => 'success',
                'message' => 'Audio generado correctamente'
            ]);
        }


        //ultimos 5 turnos atendidos
        $sqlUT = "select a.id, a.turno, a.idCaja, c.nombre from atencion a
                inner join turnos t on t.id = a.idTurno
                inner join clientes c on t.idCliente = c.id order by t.id desc limit 5";
        $errorUT = "Error al cargar los ultimos 5 turnos atendidos";
        $searchUT = consulta($con, $sqlUT, $errorUT);

        ?>

        <header>

            <div class="marco-tablaTurnos">

                <div class="contenedor-tablaTurnos">
                    <div class="columna-tablaTurnos">
                        <div class="columna-tablaTurnos c1">
                            <div class="cont-logo">
                                <img src="<?php echo $info['logo']; ?>">
                            </div>
                        </div>
                    </div>
                    <div class="columna-tablaTurnos">
                        <div class="columna-tablaTurnos c2">
                            <div class="tabla-turnosArriba">Turno</div>
                            <div class="tabla-turnosAbajo" id="verTurno"><?php echo $numeroTurno; ?></div>
                        </div>
                    </div>
                    <div class="columna-tablaTurnos">
                        <div class="columna-tablaTurnos c3">
                            <div class="tabla-turnosArriba">Ventanilla</div>
                            <div class="tabla-turnosAbajo" id="verCaja"><?php echo $caja; ?></div>
                        </div>
                    </div>
                    <div class="columna-tablaTurnos">
                        <div class="columna-tablaTurnos c3">
                            <div class="tabla-turnosArriba">Usuario</div>
                            <div class="tabla-turnosAbajo" id="verCliente"><?php echo $cliente; ?></div>
                        </div>
                    </div>
                </div>                
            </div>
        </header>

        <section class="contenido">

            <div class="contenido-izquierda">
                <div class="contenedor-video">
                    <div class="contenedor-reproductor">
                        <video id="video-geoportal" autoplay loop muted>
                            <source src="img/VID_20240516_ACC.mp4" type="video/mp4">
                        </video>
                    </div>
                </div>
            </div>
            <div class="contenido-derecha">

                <div class="contenedor-turnos">

                    <table class="tabla-turnos" id="tabla-turnos">
                        <tr>
                            <th>Turno</th>
                            <th colspan="1">Vent</th>
                            <th colspan="1">Usuario</th>
                        </tr>
                        <?php

                        if (mysqli_num_rows($searchUT) != 0) {

                            $c = 0;
                            $data = '';

                            while ($row = mysqli_fetch_assoc($searchUT)) {

                                //if($c > 0){
                                    $nombreCompleto = ucwords(strtolower($row['nombre']));
                                    $nombreArray = explode(' ', $nombreCompleto);
                                    $primerNombre = $nombreArray[0];
                                    $primerApellido = isset($nombreArray[2]) ? $nombreArray[2][0] : (isset($nombreArray[1]) ? $nombreArray[1][0] : '');
                                    $nombreFormateado = $primerNombre . ' ' . $primerApellido;
                        
                                $data .= $row['turno'] . '|' . $row['idCaja'] . '|' . $nombreFormateado . '|tr|';

                                
                                echo "<tr>
                                        <td><span  class='primer-fila'>$row[turno]</span></td>
                                        <td class='no-caja'><span  class='primer-fila'>$row[idCaja]</span></td>
                                        <td class='no-caja'><span  class='primer-fila'>$nombreFormateado</span></td>
                                    </tr>";

                                $c++;

                            }

                        }

                        ?>

                    </table>

                    <input type="hidden" name="turnos" id="turnos" value="<?php echo $data; ?>">

                </div><!--contenedor turnos-->

            </div>

        </section><!--contenido-->

        <footer class="footer">

            <marquee class="noticias">La Agencia Catastral de Cundinamarca, está comprometida con brindar el mejor
                servicio para sus diferentes públicos de interés. En este espacio de atención podrá ser parte activa de
                la Agencia y acceder a servicios y trámites.</marquee>

        </footer>


    </div><!--contenedor principal-->

    <audio src="tonos/hangouts_message.ogg" id="tono"></audio>
    <audio src="tonos/hangouts_message.ogg" id="audio"></audio>
    <script src="js/funcionesGenerales.js"></script>
    <script src="js/websocket.js"></script>

</body>

</html>