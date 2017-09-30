from django.db import models
from datetime import datetime,date,time,timedelta
from django.core.exceptions import ValidationError

# Create your models here.



class Caja(models.Model):
	trl_num = models.CharField(max_length=20)
	serial = models.CharField(max_length=20)
	id_faricante = models.ForeignKey('Fabricante')
	anio_Fab = models.IntegerField()
	id_capacidad = models.ForeignKey('Capacidad')

	def __str__(self):
		return(self.trl_num)



class Fabricante(models.Model):
	nombre = models.CharField(max_length=100)
	fecha_alta = models.DateTimeField()

	def __str__(self):
		return(self.nombre)

class Capacidad(models.Model):
	nombre = models.CharField(max_length=100)
	fecha_alta = models.DateTimeField()

	def __str__(self):
		return(self.nombre)

class Inspeccion(models.Model):
	E = 'E'
	S = 'S'
	fecha_alta = models.DateTimeField()
	id_caja = models.ForeignKey('Caja',)
	numero_sello = models.CharField(max_length=20)
	id_tractor = models.ForeignKey('Unidad')
	tipo_inspeccion = models.CharField(choices= ((E,'ENTRADA'),(S,'SALIDA'),),max_length=1)

	def __str__(self):
		return(self.id)

class InspeccionDetalle(models.Model):
	OK = 'OK'
	BA = 'BA'
	id_inspeccion = models.ForeignKey('Inspeccion')
	id_elemento = models.ForeignKey('Elemento')
	observaciones =  models.CharField(max_length=1000)
	imagen = models.ImageField()  #instalar pillow para manejar este campo
	status = models.CharField(choices=((OK,'CORRECTO'),(BA,'AVERIA'),),max_length=2)
	es_llanta = models.BooleanField()

	def __str__(self):
		return(self.id)

class InspeccionLLantas(models.Model):

	LFO = 'LFO'
	LFI = 'LFI'
	LRO = 'LRO'
	LRI = 'LRI'
	RFO = 'RFO'
	RFI = 'RFI'
	RRO = 'RRO'
	RRI = 'RRI'

	OPCIONES_DE_POSICION = ((LFO,'LFO'),(LFI,'LFI'),(LRO,'LRO'),(LRI,'LRI'),(RFO,'RFO'),(RFI,'RFI'),(RRO,'RRO'),(RRI,'RRI'),)
        
	posicion= models.CharField(max_length=3,
		choices = OPCIONES_DE_POSICION,default=LFO,
		)
	dot_tracking_num = models.CharField(max_length=12)
	id_inspecciondetalle = models.ForeignKey('InspeccionDetalle')
	id_llanta = models.ForeignKey('LLantas')
	psi = models.IntegerField()
	Profundidad = models.CharField(max_length=12)

	def __str__(self):
		return(self.id)
	

class Elemento(models.Model):
	descripcion = models.CharField(max_length=40)
	id_catagoria = models.ForeignKey('CategoriaElementosInspeccionar')

	def __str__(self):
		return(self.descripcion)

# El siguiente modelo almacena los
class CategoriaElementosInspeccionar(models.Model):
	descripcion = models.CharField(max_length=40)

	def __str__(self):
		return(self.descripcion)

class Operador(models.Model):

	nombre = models.CharField(max_length=100)
	ap_paterno = models.CharField(max_length=100)
	ap_materno =  models.CharField(max_length=100)
	telefono_particular = models.CharField(max_length=10)
	telefono_celular = models.CharField(max_length=10)
	email = models.EmailField()
	status_operador = models.ForeignKey('StatusDeOperador')
	fecha_alta = models.DateTimeField(default=datetime.now())
	fecha_baja = models.DateTimeField(default=datetime.now())
	id_tipovisa = models.ForeignKey('TipoVisa')

	
	def clean(self):
		print(self.fecha_baja)
		print(self.fecha_alta)
		print(self.telefono_celular)
		
		if self.fecha_baja is not None:
		
			if self.fecha_baja.date() < self.fecha_alta.date():
			
				raise ValidationError('La Fecha de baja debe ser mayor o igual a la fecha de alta !')
						
		else:
				raise ValidationError("La fecha retorna None !")

	
	def __str__(self):
		return '%s %s %s %s' % (self.id, self.nombre, self.ap_paterno,self.ap_materno)

	def save(self):
		self.nombre = self.nombre.upper()
		self.ap_materno = self.ap_materno.upper()
		self.ap_paterno = self.ap_paterno.upper()
		self.email = self.email.lower()
		#self.fecha_alta = datetime.now() # Asigna la fecha de hoy..antes de salvarse.
		super(Operador, self).save()

		
class Unidad(models.Model):
	id_tipounidad = models.ForeignKey('TipoUnidad')
	numero_tractor = models.CharField(max_length=12)
	placas = models.CharField(max_length=12)

	def __str__(self):
		return(str(self.id))

class TipoUnidad(models.Model):
	descripcion = models.CharField(max_length=40)

	def __str__(self):
		return(self.descripcion)

	def save(self):	
		self.descripcion = self.descripcion.upper()
		super(TipoUnidad,self).save()


class TipoVisa(models.Model):
	descripcion = models.CharField(max_length=40)

	def __str__(self):
		return(self.descripcion)

	def save(self):	
		self.descripcion = self.descripcion.upper()
		super(TipoVisa,self).save()

class OperadorEvento(models.Model):
	id_operador = models.ForeignKey('Operador')
	id_status = models.ForeignKey ('StatusDeOperador')
	fecha_inicio = models.DateTimeField()
	Fecha_terminal = models.DateTimeField()
	Comentario_extendido = models.CharField(max_length=500)

	def __str__(self):
		return '%s' %(self.id_status)

	def save(self):	
		self.Comentario_extendido = self.Comentario_extendido.upper()
		super(OperadorEvento,self).save()

class StatusDeOperador(models.Model):
	descripcion = models.CharField(max_length=40)

	def __str__(self):
		return '%s %s' %(self.id,self.descripcion)

	def save(self):	
		self.descripcion = self.descripcion.upper()
		super(StatusDeOperador,self).save()

class Llantas(models.Model):
	fabricante = models.ForeignKey('Fabricante')
	dot_tracking_num = models.CharField(max_length=12)
	fecha_alta = models.DateTimeField()
	fecha_baja = models.DateTimeField()
	Presion_max= models.CharField(max_length=12)
	numero_serie = models.CharField(max_length=20)

	def __str__(self):
		return(self.numero_serie)




