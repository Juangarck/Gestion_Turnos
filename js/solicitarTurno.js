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

function procesarSolicitud() {
    if (conexion.readyState === 4 && conexion.status === 200) {
        try {
            var jsonData = JSON.parse(conexion.responseText);
            if (jsonData.status === 'success') {
                // Mostrar número de turno u otro mensaje de éxito
                var noTurno = document.getElementById('turno');
                noTurno.innerHTML = jsonData.message;
            } else if (jsonData.status === 'error') {
                // Redirigir al registro si el cliente no existe
                window.location.href = 'registro.php';
            }
        } catch (e) {
            console.error('Error al procesar la respuesta JSON', e);
        }
    }
}