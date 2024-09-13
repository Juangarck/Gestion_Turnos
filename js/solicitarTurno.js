//agregarEvento(window, 'load', iniciar, false);
/*
function iniciar(){
    var solicitar = document.getElementById('formCedula');
    if(solicitar) {  // Verificar si el elemento existe
        agregarEvento(solicitar, 'submit', detectarAccion, false);
    } else {
        console.error('Elemento con ID "formCedula" no encontrado.');
    }
}*/
/*
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
*/
//funcion ajax que captura info de cedula
$('#formCedula').submit(function(){
    var cedula = $('#cedula').val();
    
    //aca se previene que no se recargue la pagina por el formulario
    event.preventDefault();  
    
    $.ajax({
        url:'verificar_cedula.php',
        type: 'POST',
        data: {
            cedula: cedula
        },
        dataType: 'json',
        success: function(data){
            var resultado = data.respuesta;
            if(!resultado){
                window.location.href = 'registro.php';
            }else{

                $.ajax({
                    url: 'consultas/registrar.php',
                    type: 'POST',
                    data: {
                        registrar: 'turno',
                        cedula: data.cedula },
                    dataType: 'json',
                    success: function(data2){
                        var estado = data2.status;
                        if(estado == "success"){
                            swal.fire({
                                title: "Turno: "+data2.turno,
                                html: "<b>Nombre:</b> "+data.nombre+"<br/> <b>Cédula:</b> "+data.cedula
                                +"<br/> <strong>RECUERDA ACERCARTE CON TU CÉDULA </strong>",
                                icon: "info",
                                showConfirmButton: false,
                                timer: 10000
                              }); 
                              
                              
                              setTimeout(function() {
                                location.reload();  
                                // Recargar la página despues del tiempo de mostrar el mensaje para que se actualice el de turnos (esto se puede mejorar a futuro)
                            }, 10000);
                        }else{
                            window.location.href = 'registro.php';
                        }
                        
                        
                    },
                    error: function(xhr, status, error) {
                        console.error("Error en la solicitud de registrar el turno:", error);
                    }
                }); 
            }
        }
    })
});