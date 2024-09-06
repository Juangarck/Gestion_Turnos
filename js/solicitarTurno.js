agregarEvento(window, 'load', iniciar, false);

function iniciar(){
    var solicitar = document.getElementById('formCedula');
    if(solicitar) {  // Verificar si el elemento existe
        agregarEvento(solicitar, 'submit', detectarAccion, false);
    } else {
        console.error('Elemento con ID "formCedula" no encontrado.');
    }
}

function detectarAccion(e){
    var id = "";
    
    if(e){
        id = e.target.id;
    }

    switch(id){
        case'formCedula':    
            var cedula = document.getElementById('cedula').value;
            funcion = procesarSolicitud;
            fichero = 'consultas/registrar.php';
            datos = 'registrar=turno&cedula=' + cedula;
        break;
        default:
            console.log('Opcion no reconocida');
        break;
    }
    
    conectarViaPost(funcion,fichero,datos);
}

function procesarSolicitud(){

    if(conexion.readyState === 4 && conexion.status === 200){
        try {
            var jsonData = JSON.parse(conexion.responseText);
            var noTurno = document.getElementById('turno');
            noTurno.innerHTML = jsonData.turno;
        } catch(e) {
            console.error('Error al procesar la respuesta JSON', e);
        }
    }    

}