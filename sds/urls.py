from django.conf.urls import url

from sds import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'lista_operadores/$',views.lista_operadores,name='lista_operadores'),
    url(r'lista_cajas/$',views.lista_cajas,name = 'lista_cajas'),
    url(r'crea_operador/$',views.crea_operador,name='crea_operador'),
    url(r'modifica_operador/(?P<id>[0-9]+)/$',views.modifica_operador,name='modifica_operador'),
    url(r'elimina_operador/(?P<id>[0-9]+)/$',views.elimina_operador,name='elimina_operador'),
    url(r'crea_caja/$',views.crea_caja,name='crea_caja'),
    url(r'modifica_caja/(?P<id>[0-9]+)/$',views.modifica_caja,name='modifica_caja'),
    url(r'elimina_caja/(?P<id>[0-9]+)/$',views.elimina_caja,name='elimina_caja'),
    url(r'pregunta_eliminar_operador/(?P<id>[0-9]+)/$',views.pregunta_eliminar_operador,name='pregunta_eliminar_operador'),
    url(r'pregunta_eliminar_caja/(?P<id>[0-9]+)/$',views.pregunta_eliminar_caja,name='pregunta_eliminar_caja'),
    url(r'lista_unidades/$',views.lista_unidades,name = 'lista_unidades'),
    url(r'crea_unidad/$',views.crea_unidad,name='crea_unidad'),
    url(r'modifica_unidad/(?P<id>[0-9]+)/$',views.modifica_unidad,name='modifica_unidad'),
    url(r'pregunta_eliminar_unidad/(?P<id>[0-9]+)/$',views.pregunta_eliminar_unidad,name='pregunta_eliminar_unidad'),
    url(r'lista_tipodevisa/$',views.lista_tipodevisa,name = 'lista_tipodevisa'),
    url(r'crea_tipodevisa/$',views.crea_tipodevisa,name='crea_tipodevisa'),
    url(r'elimina_tipodevisa/(?P<id>[0-9]+)/$',views.elimina_tipodevisa,name='elimina_tipodevisa'),
    url(r'modifica_tipodevisa/(?P<id>[0-9]+)/$',views.modifica_tipodevisa,name='modifica_tipodevisa'),
    url(r'pregunta_eliminar_tipodevisa/(?P<id>[0-9]+)/$',views.pregunta_eliminar_tipodevisa,name='pregunta_eliminar_tipodevisa'),
    url(r'lista_tipodeunidad/$',views.lista_tipodeunidad,name = 'lista_tipodeunidad'),
    url(r'crea_tipodeunidad/$',views.crea_tipodeunidad, name = 'crea_tipodeunidad'),
    url(r'elimina_tipodeunidad/(?P<id>[0-9]+)/$',views.elimina_tipodeunidad,name='elimina_tipodeunidad'),
    url(r'modifica_tipodeunidad/(?P<id>[0-9]+)/$',views.modifica_tipodeunidad,name='modifica_tipodeunidad'),
    url(r'pregunta_eliminar_tipodeunidad/(?P<id>[0-9]+)/$',views.pregunta_eliminar_tipodeunidad,name='pregunta_eliminar_tipodeunidad'),
    url(r'crea_operador_evento/$',views.crea_operador_evento,name='crea_operador_evento'),
    url(r'pruebadatepicker/$',views.pruebadatepicker,name='crea_pruebadatepicker'),
	url(r'busca_operador/$',views.busca_operador,name='busca_operador'),    
	url(r'busca_evento/$',views.busca_evento,name='busca_evento'),    
	url(r'eventos/$',views.eventos,name='eventos'),
    ]

