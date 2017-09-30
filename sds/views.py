from django.shortcuts import render,render_to_response
from sds.models import Operador,Caja,Unidad,TipoVisa, TipoUnidad, OperadorEvento,StatusDeOperador
import pdb
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from sds.forms import OperadorForm,CajaForm, UnidadForm,TipoVisaForm, TipoUnidadForm, OperadorEventoForm,EventoFiltroForm
from django.core.urlresolvers import reverse
from datetime import datetime,date,time,timedelta
from django.db.models import Q
import json
from django.db import connection,DatabaseError,Error,transaction,IntegrityError



def index(request):
    return HttpResponse("Hola, esta es mi aplicacion selectds.")

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    	]
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def lista_operadores(request):

	cursor=connection.cursor()
	cursor.execute("SELECT o.id,o.nombre,o.ap_paterno,o.ap_materno,s.descripcion FROM sds_operador o INNER JOIN sds_statusdeoperador s ON (o.status_operador_id=s.id) ORDER BY o.ap_paterno" )
	consulta = dictfetchall(cursor)
	'''consulta=json.dumps(l)'''
	return render(request,'sds/lista_operadores.html',{'consulta':consulta,})



	'''consulta = Operador.objects.order_by('ap_paterno')
	string_a_buscar=''
	return render(request,'sds/lista_operadores.html',{'consulta':consulta,'string_a_buscar':string_a_buscar})'''

def lista_cajas(request):
	consulta = Caja.objects.order_by('trl_num')
	return render(request,'sds/lista_cajas.html',{'consulta':consulta,})

def lista_unidades(request):
	consulta = Unidad.objects.order_by('numero_tractor')
	return render(request,'sds/lista_unidades.html',{'consulta':consulta,})

def lista_tipodevisa(request):
	consulta = TipoVisa.objects.order_by('descripcion')
	return render(request,'sds/lista_tipodevisa.html',{'consulta':consulta,})

def lista_tipodeunidad(request):
	consulta = TipoUnidad.objects.order_by('descripcion')
	return render(request,'sds/lista_tipodeunidad.html',{'consulta':consulta,})

def busca_operador(request):
	
	string_a_buscar = request.GET.get('string_a_buscar',None)
	
	if request.is_ajax() and request.method == 'GET':
		
		valor ="'%"+string_a_buscar.strip()+"%'"

		id_a_buscar='0'	
		
		if string_a_buscar.isdigit(): # verifica si la cadena a buscar es un digito, de ser asi, usara esa cadana para buscar por id.

			id_a_buscar = string_a_buscar
		

		cursor=connection.cursor()
		
		
		cursor.execute("SELECT o.id,o.nombre,o.ap_paterno,o.ap_materno,s.descripcion FROM sds_operador o INNER JOIN sds_statusdeoperador s ON (o.status_operador_id=s.id) WHERE o.id="+id_a_buscar+" or o.nombre like "+valor+" or o.ap_paterno like "+valor+" or o.ap_materno like "+valor+" or s.descripcion like "+valor+";")
		l = dictfetchall(cursor)
		
		data= json.dumps(l)
				
		return HttpResponse(data,content_type='application/json')




def crea_operador(request):
    # if this is a POST request we need to process the form data

	#pdb.set_trace()
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		form = OperadorForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
            # Interrumpe commit para validar fecha_baja ya que validacion en la forma
            # se complica, una porque no pueden ser nullas y otra porque no se les puede
            # asignar un valor de inicio ( esto se haria a nivel del modelo y django no lo permite
            # debido a que en el ModelForm se tiene definido que este campo esta deshabilitado)

            # )

			f1= form.save(commit=False)

			f1.fecha_alta=datetime.now()
			
			if f1.fecha_baja is None:

				f1.fecha_baja=datetime.now()

			f1.save()
			
			return HttpResponseRedirect('sds/crea_operador/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = OperadorForm()
		print (form)
	return render(request, 'sds/crea_operador.html', {'form': form})
	


def modifica_operador(request,id):

	registro = Operador.objects.get(pk=id) 
	

    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:

		form = OperadorForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():

			# Asigna datos normalizados a nuevas varialbles:
			
			nombre = form.cleaned_data['nombre']
			ap_paterno = form.cleaned_data['ap_paterno']
			ap_materno =  form.cleaned_data['ap_materno']
			telefono_particular = form.cleaned_data['telefono_particular']
			telefono_celular = form.cleaned_data['telefono_celular']
			email = form.cleaned_data['email']
			status_operador = form.cleaned_data['status_operador']
			#fecha_alta = form.cleaned_data['fecha_alta']
			fecha_baja = form.cleaned_data['fecha_baja']
			id_tipovisa = form.cleaned_data['id_tipovisa']
			
			# Asigna a campos de registro valores de nuevas variables con contenidos normalizados:
			# (observar como el campo id no se le asigna nada...de)
			
			registro.nombre = nombre
			registro.ap_paterno = ap_paterno
			registro.ap_materno = ap_materno
			registro.telefono_celular = telefono_celular
			registro.telefono_particular = telefono_particular
			registro.email = email
			registro.status_operador = status_operador
			#registro.fecha_alta = fecha_alta <--la fecha de alta no debe modificarse
			registro.fecha_baja = fecha_baja
			registro.id_tipovisa = id_tipovisa
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			registro.save()
			
			return HttpResponseRedirect('sds/lista_operadores/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = OperadorForm(instance=registro)
		
	return render(request, 'sds/modifica_operador.html', {'form': form,'id_op':id})


	# CREA CAJA

def crea_caja(request):
    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		form = CajaForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			form.save()
			return HttpResponseRedirect('sds/crea_caja/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = CajaForm()
	return render(request, 'sds/crea_caja.html', {'form': form})

# MODIFICA CAJA

def modifica_caja(request,id):

	registro = Caja.objects.get(pk=id) 

    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:

		form = CajaForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():

			# Asigna datos normalizados a nuevas varialbles:

			trl_num = form.cleaned_data['trl_num']
			serial = form.cleaned_data['serial']
			id_faricante =  form.cleaned_data['id_faricante']
			anio_fab = form.cleaned_data['anio_fab']
			id_capacidad = form.cleaned_data['id_capacidad']
			
			
			# Asigna a campos de registro valores de nuevas variables con contenidos normalizados:
			# (observar como el campo id no se le asigna nada...de)

			registro.trl_num = trl_num
			registro.serial = serial
			registro.id_fabricante = id_faricante
			registro.anio_fab = anio_fab
			registro.id_capacidad= id_capacidad
			
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			registro.save()
			
			return HttpResponseRedirect('sds/lista_cajas/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = CajaForm(instance=registro)
	return render(request, 'sds/modifica_caja.html', {'form': form})

def elimina_operador(request,id):

	try:
		registro = Operador.objects.get(pk=id)
		registro.delete()
		return HttpResponseRedirect('sds/lista_operadores')
	except:
		mensaje = " El registro en cuestion no fue encontrado en la base de datos, no se pudo completar la operacion  !"
		return render(request,'sds/404.html',{ 'mensaje': mensaje})

def elimina_caja(request,id):

	try:
		registro = Caja.objects.get(pk=id)
		registro.delete()
		return render(request,'sds/lista_cajas')
	except:
		mensaje = " El registro en cuestion no fue encontrado en la base de datos, no se pudo completar la operacion  !"
		return render(request,'sds/404.html',{ 'mensaje': mensaje})

def pregunta_eliminar_operador(request,id):
	return render(request,'sds/pregunta_eliminar_operador.html',{'id':id})

def pregunta_eliminar_caja(request,id):
	return render(request,'sds/pregunta_eliminar_caja.html',{'id':id})

# ------ UNIDADES ---------------


def crea_unidad(request):
    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		form = UnidadForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			form.save()
			return HttpResponseRedirect('sds/crea_unidad/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = UnidadForm()
	return render(request, 'sds/crea_unidad.html', {'form': form})

# MODIFICA CAJA

def modifica_unidad(request,id):

	registro = Unidad.objects.get(pk=id) 

    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:

		form = UnidadForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():

			# Asigna datos normalizados a nuevas varialbles:

			id_tipounidad= form.cleaned_data['id_tipounidad']
			numero_tractor = form.cleaned_data['numero_tractor']
			placas =  form.cleaned_data['placas']
			
			
			
			# Asigna a campos de registro valores de nuevas variables con contenidos normalizados:
			# (observar como el campo id no se le asigna nada...de)

			registro.id_tipounidad = id_tipounidad
			registro.numero_tractor = numero_tractor
			registro.placas = placas
			
			
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			registro.save()
			
			return HttpResponseRedirect('sds/lista_unidades/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = UnidadForm(instance=registro)
	return render(request, 'sds/modifica_unidad.html', {'form': form})

def elimina_unidad(request,id):

	try:
		registro = Unidad.objects.get(pk=id)
		registro.delete()
		return HttpResponseRedirect('sds/lista_unidades')
	except:
		mensaje = " El registro en cuestion no fue encontrado en la base de datos, no se pudo completar la operacion  !"
		return render(request,'sds/404.html',{ 'mensaje': mensaje})

def pregunta_eliminar_unidad(request,id):
	return render(request,'sds/pregunta_eliminar_unidad.html',{'id':id})



# TIPOS DE VISA********************************************

def crea_tipodevisa(request):
    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		form = TipoVisaForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			form.save()
			return HttpResponseRedirect('sds/crea_tipodevisa/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = TipoVisaForm()
	return render(request, 'sds/crea_tipodevisa.html', {'form': form})

# MODIFICA CAJA

def modifica_tipodevisa(request,id):

	registro = TipoVisa.objects.get(pk=id) 

    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:

		form = TipoVisaForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():

			# Asigna datos normalizados a nuevas varialbles:

			descripcion = form.cleaned_data['descripcion']
			
			
			
			# Asigna a campos de registro valores de nuevas variables con contenidos normalizados:
			# (observar como el campo id no se le asigna nada...de)

			registro.descripcion = descripcion
			
			
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			registro.save()
			
			return HttpResponseRedirect('sds/lista_tipodevisa/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = TipoVisaForm(instance=registro)
	return render(request, 'sds/modifica_tipodevisa.html', {'form': form})



def elimina_tipodevisa(request,id):

	try:
		registro = TipoVisa.objects.get(pk=id)
		registro.delete()
		return HttpResponseRedirect('sds/lista_tipodevisa')
	except:
		mensaje = " El registro en cuestion no fue encontrado en la base de datos, no se pudo completar la operacion  !"
		return render(request,'sds/404.html',{ 'mensaje': mensaje})

def pregunta_eliminar_tipodevisa(request,id):
	return render(request,'sds/pregunta_eliminar_tipodevisa.html',{'id':id})


#	****************  TIPO DE UNIDAD ************


def crea_tipodeunidad(request):
    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		form = TipoUnidadForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			form.save()
			return HttpResponseRedirect('sds/crea_tipodeunidad/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = TipoUnidadForm()
	return render(request, 'sds/crea_tipodeunidad.html', {'form': form})

# MODIFICA CAJA

def modifica_tipodeunidad(request,id):

	registro = TipoUnidad.objects.get(pk=id) 

    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:

		form = TipoUnidadForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():

			# Asigna datos normalizados a nuevas varialbles:

			descripcion = form.cleaned_data['descripcion']
			
			
			
			# Asigna a campos de registro valores de nuevas variables con contenidos normalizados:
			# (observar como el campo id no se le asigna nada...de)

			registro.descripcion = descripcion
			
			
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			registro.save()
			
			return HttpResponseRedirect('sds/lista_tipodeunidad/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = TipoUnidadForm(instance=registro)
	return render(request, 'sds/modifica_tipodeunidad.html', {'form': form})



def elimina_tipodeunidad(request,id):

	try:
		registro = TipoUnidad.objects.get(pk=id)
		registro.delete()
		return HttpResponseRedirect('sds/lista_tipodeunidad')
	except:
		mensaje = " El registro en cuestion no fue encontrado en la base de datos, no se pudo completar la operacion  !"
		return render(request,'sds/404.html',{ 'mensaje': mensaje})

def pregunta_eliminar_tipodeunidad(request,id):
	return render(request,'sds/pregunta_eliminar_tipodeunidad.html',{'id':id})


#	****************  Operador Evento ************


def crea_operador_evento(request):
    # if this is a POST request we need to process the form data
	
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		form = OperadorEventoForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			print ("paso por aqui")
			form.save()
			return HttpResponseRedirect('sds/crea_operador_evento/')
		else:
			pass

    # if a GET (or any other method) we'll create a blank form
	else:
		form = OperadorEventoForm()
	return render(request, 'sds/crea_operadorevento.html', {'form': form})

def pruebadatepicker(request):
    # if this is a POST request we need to process the form data

	#pdb.set_trace()
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		form = ToDoForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			form.save()
			return HttpResponseRedirect('sds/pruebadatepicker/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = ToDoForm()
		print (form)
	return render(request, 'sds/template.html', {'form': form})


def formatea_fecha(p_fecha):
	dia = p_fecha[0:2]
	mes = p_fecha[3:5]	
	anio = p_fecha[6:10]
	hora = p_fecha[11:]
	nueva_fecha = anio+'-'+mes+'-'+dia+' '+hora
	print ("la nueva fecha es:")
	print(nueva_fecha)
	return nueva_fecha

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")
	
def busca_evento(request):


	pdb.set_trace()
	
	operador = request.GET.get('operador_id',None)
	status = request.GET.get('status_id',None)
	fecha_inicial = formatea_fecha(request.GET.get('fecha_inicial',None))
	fecha_final = formatea_fecha(request.GET.get('fecha_final',None))
	comentario_extendido = request.GET.get('comentario_extendido',None)

	print (operador)
	print (status)
	print (fecha_inicial)
	print (fecha_final)
	print (comentario_extendido)


	
	if request.is_ajax() and request.method == 'GET':

		
		
		com_ext ="'%"+comentario_extendido.strip()+"%'"

		cursor=connection.cursor()

		# no, no , si
		
		if(operador is '' and status is '' and comentario_extendido is not ''):
			
			cursor.execute("SELECT oe.id,o.nombre,o.ap_paterno,o.ap_materno,s.descripcion,oe.fecha_inicio,oe.Fecha_Terminal,oe.Comentario_extendido FROM sds_operadorevento oe INNER JOIN sds_statusdeoperador s ON (oe.id_status_id=s.id) INNER JOIN sds_operador o on (oe.id_operador_id=o.id) WHERE oe.comentario_extendido like "+com_ext+" and oe.fecha_inicio >=%s and oe.fecha_inicio<=%s;",(fecha_inicial,fecha_final))
		
		# no, si, no			
		if(operador is '' and status is not '' and comentario_extendido is ''):

			cursor.execute("SELECT oe.id,o.nombre,o.ap_paterno,o.ap_materno,s.descripcion,oe.fecha_inicio,oe.Fecha_Terminal,oe.Comentario_extendido FROM sds_operadorevento oe INNER JOIN sds_statusdeoperador s ON (oe.id_status_id=s.id) INNER JOIN sds_operador o on (oe.id_operador_id=o.id) WHERE oe.id_status_id="+status+" and oe.fecha_inicio >=%s and oe.fecha_inicio<=%s;",(fecha_inicial,fecha_final))
		# no, si , si
		if(operador is '' and status is not '' and comentario_extendido is not ''):
	
			cursor.execute("SELECT oe.id,o.nombre,o.ap_paterno,o.ap_materno,s.descripcion,oe.fecha_inicio,oe.Fecha_Terminal,oe.Comentario_extendido FROM sds_operadorevento oe INNER JOIN sds_statusdeoperador s ON (oe.id_status_id=s.id) INNER JOIN sds_operador o on (oe.id_operador_id=o.id) WHERE oe.comentario_extendido like "+com_ext+" and oe.id_status_id=%s and oe.fecha_inicio >=%s and oe.fecha_inicio<=%s;",(status,fecha_inicial,fecha_final))
		# si, no , no
		if(operador is not '' and status is '' and comentario_extendido is ''):
	
			cursor.execute("SELECT oe.id,o.nombre,o.ap_paterno,o.ap_materno,s.descripcion,oe.fecha_inicio,oe.Fecha_Terminal,oe.Comentario_extendido FROM sds_operadorevento oe INNER JOIN sds_statusdeoperador s ON (oe.id_status_id=s.id) INNER JOIN sds_operador o on (oe.id_operador_id=o.id) WHERE oe.id_operador_id=%s and oe.fecha_inicio >=%s and oe.fecha_inicio<=%s;",(operador,fecha_inicial,fecha_final))

		# si, no , si
		if(operador is not '' and status is '' and comentario_extendido is not ''):
	
			cursor.execute("SELECT oe.id,o.nombre,o.ap_paterno,o.ap_materno,s.descripcion,oe.fecha_inicio,oe.Fecha_Terminal,oe.Comentario_extendido FROM sds_operadorevento oe INNER JOIN sds_statusdeoperador s ON (oe.id_status_id=s.id) INNER JOIN sds_operador o on (oe.id_operador_id=o.id) WHERE oe.id_operador_id=%s and oe.comentario_extendido like"+com_ext+" and oe.fecha_inicio >=%s and oe.fecha_inicio<=%s;",(operador,fecha_inicial,fecha_final))
		# si, si , no
		if(operador is not '' and status is not '' and comentario_extendido is ''):
			print("Entro en si,si no")
	
			cursor.execute("SELECT oe.id,o.nombre,o.ap_paterno,o.ap_materno,s.descripcion,oe.fecha_inicio,oe.Fecha_Terminal,oe.Comentario_extendido FROM sds_operadorevento oe INNER JOIN sds_statusdeoperador s ON (oe.id_status_id=s.id) INNER JOIN sds_operador o on (oe.id_operador_id=o.id) WHERE oe.id_operador_id=%s and oe.id_status_id=%s and oe.fecha_inicio >=%s and oe.fecha_inicio<=%s;",(operador,status,fecha_inicial,fecha_final))

			for c in cursor:
				print (c)

			#return HttpResponse(data,content_type='application/txt')





		
			#cursor.execute("SELECT oe.id,o.nombre,o.ap_paterno,o.ap_materno,s.descripcion,oe.fecha_inicio,oe.Fecha_Terminal,oe.Comentario_extendido FROM sds_operadorevento oe INNER JOIN sds_statusdeoperador s ON (oe.id_status_id=s.id) INNER JOIN sds_operador o on (oe.id_operador_id=o.id) WHERE oe.id_status_id="+status+" or oe.id_operador_id="+operador+" and oe.fecha_inicio >=%s and oe.fecha_inicio<=%s;",(fecha_inicial,fecha_final))
	l = dictfetchall(cursor)
		#print ("paso el SELECT")
	
	data= json.dumps(l,default=datetime_handler)
				
	return HttpResponse(data,content_type='application/json')
	
	
	
def eventos(request):

	# Esta funcion tiene por objeto mostrar la forma para filtrar los eventos.

	eventofiltro_form = EventoFiltroForm()
	context={'consulta':True,'eventofiltro_form':eventofiltro_form}
	print (eventofiltro_form)
	return render(request,'sds/filtra_eventos.html',context)