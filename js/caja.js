agregarEvento(window, 'load', iniciar, false);

function iniciar(){

	var atender = document.getElementById('atender');

	agregarEvento(atender,'click',detectarAccion,false);

}

var jsonFormat = '';

function detectarAccion(e){
	
	var id = "";
	
	if(e){
	
		e.preventDefault();
	
		id = e.target.id;
	
	}
	
	switch(id){
	
		case'atender':	
	
			var ocupado = document.getElementById('ocupado').value;//se usa para saber si se esta atendiendo o no un turno
			var idCaja = document.getElementById('idCaja').value;
			var turno = document.getElementById('noTurno').value;
	
			funcion = procesarAtencion;
	
			fichero = 'consultas/registrar.php';
	
			var datos = 'registrar=atencion'+'&ocupado='+encodeURIComponent(ocupado)+'&idCaja='+encodeURIComponent(idCaja)+'&turno='+encodeURIComponent(turno);
	
		break;
	
	}

	conectarViaPost(funcion, fichero, datos);

}

function procesarAtencion() {

    if (conexion.readyState == 4) {

        var data = conexion.responseText;

        // enviar los datos recibidos mediante ajax en formato json al socket
        console.log(data);
        socket.send(data);

        var jsonData = JSON.parse(data); // decodificar los datos en formato json

        var turno = document.getElementById('turno'); // turno que se muestra en la pantalla
        var noTurno = document.getElementById('noTurno'); // control input noTurno
        var cliente_atender = document.getElementById('cliente_atender'); // div donde se mostrara la información del cliente a atender
        var mensajes = document.getElementById('mensajes'); // div para los mensajes

        if (jsonData.status == 'error' || jsonData.status == 'mensaje') {
            // poner mensajes de error o de aviso
            mensajes.innerHTML = jsonData.mensaje;

            // limpiar la información del cliente y el turno
            cliente_atender.innerHTML = 'Nombre: <br/><br/>Cédula: ';
            turno.innerHTML = '';
            noTurno.value = '';
        } else {
            mensajes.innerHTML = '';
            
            // Mostrar la información del cliente si no hay errores
            var nombre = jsonData.nombre.toUpperCase();
            var cedula = jsonData.cedula;
            
            cliente_atender.innerHTML = 'Nombre: ' + nombre + "<br/><br/>Cédula: " + cedula;
            turno.innerHTML = jsonData.turno;
            noTurno.value = jsonData.turno;
            
            console.log(jsonData);
        }

    }

}
