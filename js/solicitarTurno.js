agregarEvento(window, 'load', iniciar, false);

function iniciar(){
    var solicitar = document.getElementById('solicitarTurno');
    if(solicitar) {  // Verificar si el elemento existe
        agregarEvento(solicitar, 'click', detectarAccion, false);
    } else {
        console.error('Elemento con ID "solicitarTurno" no encontrado.');
    }
}

function detectarAccion(e){
    var id = "";
    
    if(e){
        id = e.target.id;
    }

    switch(id){
        case'solicitarTurno':    
            var nombre = document.getElementById('nombre').value;
            var cedula = document.getElementById('cedula').value;
            funcion = procesarSolicitud;
            fichero = 'consultas/registrar.php';
            datos = 'registrar=turno&nombre=' + nombre + '&cedula=' + cedula;
        break;
        default:
            console.log('Opcion no reconocida');
        break;
    }
    
    conectarViaPost(funcion,fichero,datos);
}

function procesarSolicitud(){

	if(conexion.readyState === 4){

		var jsonData = JSON.parse(conexion.responseText);
		var noTurno = document.getElementById('turno');
	 
	 	noTurno.innerHTML = jsonData.turno;

	}

}