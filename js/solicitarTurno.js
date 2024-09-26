//funcion ajax que captura info de cedula
$('#formCedula').submit(function(){
    var tramite = $('#tramite').val();
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
                        cedula: cedula,
                        tramite: tramite
                     },
                    dataType: 'json',
                    success: function(data2){
                        var estado = data2.status;
                        if(estado == "success"){
                            swal.fire({
                                title: "Turno: "+data2.turno,
                                html: "<b>Nombre:</b> " + data.nombre.toUpperCase() + "<br/>" +
                                "<b>Cédula:</b> " + data.cedula + "<br/>" +
                                "<strong>RECUERDA ACERCARTE CON TU CÉDULA</strong><br/><br/>" +
                                "<small><em>De acuerdo con la Ley 1581 de 2012, usted tiene derecho a solicitar la modificación o eliminación de sus datos personales. " +
                                "Para ejercer este derecho, puede enviar un correo a <strong>atencionalciudadano@acc.gov.co</strong> con el asunto 'Modificación de datos personales digiturno'.</em></small>",
                                icon: "info",
                                showConfirmButton: false,
                                timer: 15000
                              }); 
                              
                              
                              setTimeout(function() {
                                location.reload();  
                                // Recargar la página despues del tiempo de mostrar el mensaje para que se actualice el de turnos (esto se puede mejorar a futuro)
                            }, 15000);
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