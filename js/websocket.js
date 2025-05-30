agregarEvento(window, 'load', iniciarWebsocket, false);

var imgStatus = null;

let tono = null;
let audio = null; 

function iniciarWebsocket() {

	imgStatus = document.getElementById('imgStatus');

	socket = new WebSocket("ws://192.168.43.234:8888/php/proyectos/turnero/turnero/server.php");

	socket.addEventListener('open', abierto, false);
	socket.addEventListener('message', recibido, false);
	socket.addEventListener('close', cerrado, false);
	socket.addEventListener('error', errores, false);

	tono = document.getElementById('tono');
    audio = document.getElementById("audio");
}

//se activa cuando se conecta el cliente a el socket
function abierto() {

	if (imgStatus != null) {

		imgStatus.src = "img/conectado.png";

	}
}

//funcion que recibe los mensajes del socket
function recibido(e) {
	console.log(e.data);
	var jsonData = JSON.parse(e.data);//decodificar el objeto json

	var turno = document.getElementById('verTurno');
	var caja = document.getElementById('verCaja');
	var cliente = document.getElementById('verCliente');

    // Cambia 'data' a 'jsonData'
    if (jsonData.action === 'setIdFuncionario') {
        sessionStorage.setItem('idFuncionario', jsonData.idFuncionario);
        console.log('ID Funcionario recibido:', jsonData.idFuncionario);
        return; // Añade un return para salir de la función aquí si es necesario
    }

	//si turno Viene en 000 o undefined siginfica que no hay nuevos turnos
	if (typeof jsonData.type === 'string' && jsonData.type === 'data') {

		if (typeof jsonData.turno === 'string' &&
			typeof jsonData.idCaja === 'string') {

			if (turno != null && caja != null) {

				if (jsonData != '' && jsonData.idCaja != '' && jsonData.status === 'success') {

					var nombreArray = jsonData.nombre.trim().split(' ');
					var primerNombre = nombreArray[0];
					const primerApellido = nombreArray[2] ? nombreArray[2][0] : (nombreArray[1] ? nombreArray[1][0] : '');
					var nombreFormateado = (primerNombre + " " + primerApellido).toUpperCase();

					turno.innerHTML = jsonData.turno;
					caja.innerHTML = jsonData.idCaja;
					cliente.innerHTML = nombreFormateado;
					

					mostrarTurnos(jsonData.turno, jsonData.idCaja, nombreFormateado);

				}

			}

		} else {

			console.error('El tipo de dato de turno o caja no es valido');

		}

	}

}

function cerrado() {

	if (imgStatus != null) {

		imgStatus.src = "img/desconectado.png";

	}


}

function errores() {

	if (imgStatus != null) {

		imgStatus.src = "img/error.png";

	}


}

var tr = "";

var turnsTable = [];

let newArray = [];

//mostrar los turnos que se atienden 
function mostrarTurnos(noTurno = '', noCaja = '', noNombre = '') {

	let turn = [];//array que almacenara los turnos a mostrar

	let displayedTurns = load_diplayed_turns();

	//colocar el turno que se va a atender en el array
	turn = {
        'turno': noTurno || 'N/A', // Inicializa con 'N/A' si no hay datos
        'caja': noCaja || 'N/A',
        'nombre': (noNombre || 'N/A').toUpperCase()
	};


	//verificar si ya se tienen turnos en pantalla cuando se carga el visualizador de turnos

	if (displayedTurns.length > 0 && newArray.length === 0) {

		//si hay turnos en pantalla se entra aqui

		for (let i = 0; i < displayedTurns.length; i++) {

			//generacion de array con los turnos en patalla
			if (i === 0) {

				newArray[i] = turn;

			} else {

				newArray[i] = displayedTurns[i - 1];

			}

		}

		generate_table(newArray);

	} else {

		//si no hay turnos en pantalla se entra aqui

		newArray.unshift(turn);

		if (newArray.length > 5) {

			newArray.pop();

		}

		generate_table(newArray);

	}

}

//cargar turnos que se ya se estan mostrando en pantalla
function load_diplayed_turns() {
    let turns = document.getElementById('turnos').value;

    // Verificar si el valor de turnos es válido
    if (!turns || turns === "") {
        return []; // Retorna un array vacío si no hay turnos
    }

    turns = turns.split('|tr|');

    let arrayTable = [];
    let arrayTurn = [];

    // Evitar procesar si no hay turnos válidos
    if (turns.length === 0) {
        return []; // Retorna un array vacío si no hay turnos
    }

    for (let i = 0; i < turns.length - 1; i++) {
        arrayTurn = turns[i].split('|');

        arrayTable[i] = {
            'turno': arrayTurn[0] || '', // Inicializa con cadena vacía si no existe
            'caja': arrayTurn[1] || '',
            'nombre': arrayTurn[2] || ''
        };
    }

    return arrayTable;
}


//generar la tabla con los turnos
function generate_table(table = null) {
    var th = "<tr><th>Turno</th><th colspan='1'>Vent</th><th colspan='1'>Usuario</th></tr>";

    if (table.length === 0) {
        // Si no hay datos, mostrar un mensaje de 'No hay turnos'
        tr = "<tr><td colspan='3'>No hay turnos pendientes</td></tr>";
    } else {
        for (var i = 0; i < table.length; i++) {
            if (i == 0) {
                tr = "<tr><td><span class='primer-fila'>" + table[i]['turno'] + "</span></td><td class='no-caja'><span class='primer-fila'>" + table[i]['caja'] + "</span></td><td class='no-caja'><span class='primer-fila'>" + table[i]['nombre'] + "</span></td></tr>";
            } else {
                tr = tr + "<tr><td>" + table[i]['turno'] + "</td><td class='no-caja'>" + table[i]['caja'] + "</td><td>" + table[i]['nombre'].toUpperCase() + "</td></tr>";
            }
        }
    }

    display_table(th + tr);
}


//mostrar la tabla de turnos en pantalla
function display_table(table = '') {
    var tablaTurnos = document.getElementById('tabla-turnos');

    tablaTurnos.innerHTML = table;  // Imprimir los turnos que han pasado y el turno que está siendo atendido

    tono.play();  // Reproducir el sonido de notificación

    // Esperar 500ms antes de enviar los datos al archivo PHP para ejecutar la llamada por voz
    setTimeout(function() {
        if (newArray.length > 0) {
            var turnoActual = newArray[0];
            console.log(`Enviando datos para audio: turno: ${turnoActual.turno}, caja: ${turnoActual.caja}, cliente: ${turnoActual.nombre}`);
            // Enviar solicitud POST al archivo PHP para generar el audio
            fetch('./turnos.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `numeroTurno=${turnoActual.turno}&caja=${turnoActual.caja}&cliente=${turnoActual.nombre}`
            })
            .then(response => { 
        
                // Reproducir el archivo de audio generado
                audio.src = `./tonos/turno_${turnoActual.turno}.ogg`;
                audio.play();
 
            })
            .catch(error => {
                console.error("Error en la solicitud:", error);
            });
        }
        else {
            console.error("No hay turnos disponibles en newArray");
        }
    }, 20);
}