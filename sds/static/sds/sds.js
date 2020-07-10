

    $(document).ready(function() {
            //alert("funciona !");
            //$('#datepicker').datepicker();
            //$('#datepicker').datepicker({uiLibrary: 'bootstrap4'});
            $('#busca_op').click(function(event){
               //alert("hola");
                event.preventDefault();
                $.ajax({
                        url: '/sds/busca_operador',
                        type: 'GET',
                        data: {'string_a_buscar':$('#busca_op_input').val()},
                        success: function(data,total_elementos) {
                            console.log(data);
                            var tableData = ''

                            $('tbody').empty(); // Borra tabla

                            if (data.length==0){
                                alert("No se encontraron coincidencias !")
                            };
                            tableData += "<tr><th>id</th><th>Ap paterno</th><th>Ap materno</th><th>Nombre</th><th> Status actual</th></tr>"; // Dibuja encab
                            //Ajax nos retorna en data un arreglo de arreglos..asi
                            // que primeramente "each(data....)" hace referecia a 
                            // cada arreglo dentro del arreglo y "value" nos trae
                            // el conenido de cada arreglo, asi que tenemos que hacer
                            // referencia a value[0], value[1]... etc para poder traer los campos que nos interesan.

                            $('tbody').append(
                                $.each(data, function(key,value){
                                                                        
                                    tableData += '<tr>';
                                    tableData += '<td>' +'<a href="/sds/modifica_operador/'+value['id']+'/">'+value['id'] + '</a></td>'; // link id para modificar.
                                     tableData += '<td>' + value['ap_paterno'] + '</td>';
                                     tableData += '<td>' + value['ap_materno'] + '</td>';
                                     tableData += '<td>' + value['nombre'] + '</td>';
                                     tableData += '<td>' + value['descripcion'] + '</td>';
                                     
                                     
                                     
                                    tableData += '</tr>';
                                })
                            );
                            $('#tot').text("Total de registros encontrados: "+data.length);
                            $('tbody').html(tableData); // Cambi el contenido de tbody
                            
                        },

                        error: function(data) {
                            console.log('error')
                            console.log(data)
                        }
                });
             })

            $('#busca_op_eventos').click(function(event){

              //id_operador = $('#id_operador').val();
              //id_status =  $('#id_status').val();
               //alert("hola quiko");
               //if (id_operador =! '(Todos)' && id_status =!'(Todos)') { 
               // alert(" Debe elegir un valor para operador o bien para status ( al menos uno de ellos) !");
                //hayerror = 1;
                        //} 
                event.preventDefault();
                   

                alert("entra aqui");


                $.ajax({
                        url: '/sds/busca_evento',
                        type: 'GET',
                        data: {'operador_id':$('select[name=operador]').val(),'status_id':$('select[name=status]').val(),'fecha_inicial':$('#id_fecha_inicio').val(),'fecha_final':$('#id_fecha_final').val(),'comentario_extendido':$('#id_comentario_extendido').val()},
                        success: function(data,total_elementos) {
                            alert("entro en success");
                            console.log(data);
                            var tableData 
                            $('tbody').empty(); // Borra tabla

                            if (data.length==0){
                                alert("No se encontraron coincidencias !")
                            };
                            tableData += "<tr><th>id_evento</th><th>Nombre_Operador</th><th>Status</th><th>Inicio el </th><th>Termina el</th><th>Comentario</th></tr>"; // Dibuja encab
                            //Ajax nos retorna en data un arreglo de arreglos..asi
                            // que primeramente "each(data....)" hace referecia a 
                            // cada arreglo dentro del arreglo y "value" nos trae
                            // el conenido de cada arreglo, asi que tenemos que hacer
                            // referencia a value[0], value[1]... etc para poder traer los campos que nos interesan.

                            $('tbody').append(
                                $.each(data, function(key,value){
                                                                        
                                    tableData += '<tr>';
                                    tableData += '<td>' +'<a href="/sds/modifica_operador/'+value['id']+'/">'+value['id'] + '</a></td>'; // link id para modificar.
                                     tableData += '<td>' + value['ap_paterno'] +' '+value['ap_materno']+' '+value['nombre']+'</td>';
                                     tableData += '<td>' +value['descripcion']+ '</td>';
                                     tableData += '<td>' +value['fecha_inicio']+ '</td>';
                                     tableData += '<td>' +value['Fecha_Terminal']+'</td>';
                                     tableData += '<td>' +value['Comentario_extendido']+'</td>';
                                     
                                     
                                    tableData += '</tr>';
                                })
                            );
                            $('#tot').text("Total de registros encontrados: "+data.length);
                            $('tbody').html(tableData); // Cambi el contenido de tbody
                            
                        },

                        error: function(data) {
                            alert("error en llamado ajax de filtrar eventos");
                            console.log('error');
                            console.log(data);
                        }
                        
                });
             })

    })
