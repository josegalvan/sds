from django import forms
#from bootstrap_date.widgets import DateTimePicker
from datetime import datetime,date,time,timedelta
from django.forms import ModelForm
from sds.models import Operador, Caja, Unidad,TipoVisa, TipoCaja, TipoUnidad, OperadorEvento,StatusDeOperador
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import TabHolder, Tab
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Field,HTML,Div,Button
import pdb
from functools import partial

class OperadorForm(ModelForm):
	
	
			
	helper = FormHelper()
	helper.form_tag = False
	helper.form_class = 'form'
	helper.form_style = 'inline'
	helper.layout = Layout(
			Fieldset(
			'Informacion Basica',
			'nombre',
            'ap_paterno',
            'ap_materno',
            'status_operador',
            'id_tipovisa',
            Field('fecha_alta',disabled='True'),
            Field('fecha_baja',placeholder='DD/MM/YYYY HH:MM',id='datepicker'),

            ),
	 		Fieldset(
           	'Datos de contacto',
            'telefono_particular',
            'telefono_celular',
            'email',)
	         )   
		

	class Meta:
		model = Operador
		fields = ['id','nombre', 'ap_paterno', 'ap_materno', 'telefono_particular','telefono_celular','email',
		'status_operador','fecha_alta','fecha_baja','id_tipovisa']
		widgets= {'fecha_baja': forms.DateTimeInput(attrs={'id': 'datetimepicker',})}
		

		
	def __init__(self, *args, **kwargs):
		super(OperadorForm, self).__init__(*args, **kwargs)
		self.fields['fecha_baja'].required = True
		self.fields['fecha_alta'].required = False



# formma para la Caja

class CajaForm(ModelForm):
		helper = FormHelper()
		helper.form_tag = False
		helper.form_class = 'form'
		helper.layout = Layout( 
					Fieldset('Datos de la caja',
						'trl_num', 
						'serial',
						'id_faricante',
						'anio_Fab',
						'id_capacidad')
					)
		class Meta:
			model = Caja
			fields = ['trl_num','serial','id_faricante','anio_Fab','id_capacidad']	

class UnidadForm(ModelForm):
		helper = FormHelper()
		helper.form_tag = False
		helper.form_class = 'form'
		helper.layout = Layout( 
					Fieldset('Datos de la unidad',
						'id_tipounidad', 
						'numero_tractor',
						'placas',
						)
					)
		class Meta:
			model = Unidad
			fields = ['id_tipounidad','numero_tractor','placas',]	

class TipoVisaForm(ModelForm):
		helper = FormHelper()
		helper.form_tag = False
		helper.form_class = 'form'
		helper.layout = Layout( 
					Fieldset('',
						'descripcion', 
						)
					)
		class Meta:
			model = TipoVisa
			fields = ['descripcion',]	

class TipoCajaForm(ModelForm):
		helper = FormHelper()
		helper.form_tag = False
		helper.form_class = 'form'
		helper.layout = Layout( 
					Fieldset('',
						'descripcion', 
						)
					)
		class Meta:
			model = TipoCaja
			fields = ['descripcion',]	


class TipoUnidadForm(ModelForm):
		helper = FormHelper()
		helper.form_tag = False
		helper.form_class = 'form'
		helper.layout = Layout( 
					Fieldset('',
						'descripcion', 
						)
					)
		class Meta:
			model = TipoUnidad
			fields = ['descripcion',]	

class OperadorEventoForm(ModelForm):
		helper = FormHelper()
		helper.form_tag= False
		helper.form_class = 'form'
		helper.layout = Layout(
					Fieldset('',
						'id_operador',
						'id_status',
						'fecha_inicio',
						'Fecha_terminal',
						'Comentario_extendido',
					))		
		class Meta:
			model = OperadorEvento
			fields = ['id_operador','id_status','fecha_inicio','Fecha_terminal','Comentario_extendido']
			widgets= {'Comentario_extendido': forms.Textarea(attrs={'cols': 80, 'rows': 6})}


class EventoFiltroForm(forms.Form):
	
	operador  = forms.ModelChoiceField(initial='Todos',queryset=Operador.objects.only('ap_paterno','ap_materno','nombre','id').order_by('ap_paterno'),empty_label="(Todos)",required=False)
	status = forms.ModelChoiceField(initial='Todos',queryset=StatusDeOperador.objects.all().order_by('descripcion'), empty_label="(Todos)",required=False)
	fecha_inicio = forms.DateTimeField(initial=datetime.now())
	fecha_final = forms.DateTimeField(initial=datetime.now())
	comentario_extendido = forms.CharField(widget=forms.Textarea(attrs={'rows':2}),required=False)
	def __init__(self, *args, **kwargs):
		super(EventoFiltroForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-eventoFiltroForm'
		self.helper.form_class = 'blueform'
		self.helper.form_method = 'post'
		#self.helper.form_action = 'submit_survey'
		self.helper.layout = Layout(
					Fieldset('Filtro',
						'operador',        					
						'status',
						'fecha_inicio',
						'fecha_final',						
						'comentario_extendido',
						HTML("""<div class="input-group">
                            
                               <a id="busca_op_eventos" href="" type="button" class="btn btn-primary">              
                                <i class="fa fa-search" aria-hidden="true">  Buscar eventos </i>
                                </a>
                                
                                
                                
                        </div>"""
							),
						
					))		
		

		#self.helper.add_input(Submit('submit', 'Submit'))
					

		

  