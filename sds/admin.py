from django.contrib import admin

# Register your models here.
from .models import Caja,Fabricante,Capacidad,Inspeccion,InspeccionDetalle,InspeccionLLantas,Elemento,CategoriaElementosInspeccionar,Operador,Unidad,TipoUnidad,TipoVisa,OperadorEvento,StatusDeOperador,Llantas
admin.site.register(Caja)
admin.site.register(Fabricante)
admin.site.register(Capacidad)
admin.site.register(Inspeccion)
admin.site.register(InspeccionDetalle)
admin.site.register(InspeccionLLantas)
admin.site.register(Elemento)
admin.site.register(CategoriaElementosInspeccionar)
admin.site.register(Operador)
admin.site.register(Unidad)
admin.site.register(TipoUnidad)
admin.site.register(TipoVisa)
admin.site.register(OperadorEvento)
admin.site.register(StatusDeOperador)
admin.site.register(Llantas)
