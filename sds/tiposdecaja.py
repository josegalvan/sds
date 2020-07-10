# TIPOS DE CAJA********************************************
from sds.models import TipoCaja


def lista_tipodecaja(request):
	consulta = TipoCaja.objects.order_by('descripcion')
	return render(request,'sds/lista_tipodecaja.html',{'consulta':consulta,})

def crea_tipodecaja(request):
    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		form = TipoCajaForm(request.POST)
        # check whether it's valid:
		
		if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			
			form.save()
			return HttpResponseRedirect('sds/crea_tipodecaja/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = TipoCajaForm()
	return render(request, 'sds/crea_tipodecaja.html', {'form': form})

# MODIFICA TIPO DE CAJA

def modifica_tipodecaja(request,id):

	registro = Tipocaja.objects.get(pk=id) 

    # if this is a POST request we need to process the form data
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:

		form = TipoCajaForm(request.POST)
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
			
			return HttpResponseRedirect('sds/lista_tipodecaja/')
		

    # if a GET (or any other method) we'll create a blank form
	else:
		form = TipoCajaForm(instance=registro)
	return render(request, 'sds/modifica_tipodecaja.html', {'form': form})

# ELIMINA TIPO DE CAJA

def elimina_tipodecaja(request,id):

	try:
		registro = TipoCaja.objects.get(pk=id)
		registro.delete()
		return HttpResponseRedirect('sds/lista_tipodecaja')
	except:
		mensaje = " El registro en cuestion no fue encontrado en la base de datos, no se pudo completar la operacion  !"
		return render(request,'sds/404.html',{ 'mensaje': mensaje})

def pregunta_eliminar_tipodecaja(request,id):
	return render(request,'sds/pregunta_eliminar_tipodecaja.html',{'id':id})

