# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 04:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trl_num', models.CharField(max_length=20)),
                ('serial', models.CharField(max_length=20)),
                ('anio_Fab', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Capacidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fecha_alta', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaElementosInspeccionar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Elemento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=40)),
                ('id_catagoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.CategoriaElementosInspeccionar')),
            ],
        ),
        migrations.CreateModel(
            name='Fabricante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fecha_alta', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='InpeccionLLantas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicion', models.CharField(choices=[('LFO', 'LFO'), ('LFI', 'LFI'), ('LRO', 'LRO'), ('LRI', 'LRI'), ('RFO', 'RFO'), ('RFI', 'RFI'), ('RRO', 'RRO'), ('RRI', 'RRI')], default='LFO', max_length=3)),
                ('dot_tracking_num', models.CharField(max_length=12)),
                ('psi', models.IntegerField()),
                ('Profundidad', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Inspeccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_alta', models.DateTimeField()),
                ('numero_sello', models.CharField(max_length=20)),
                ('tipo_inspeccion', models.CharField(choices=[('E', 'ENTRADA'), ('S', 'SALIDA')], max_length=1)),
                ('id_caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.Caja')),
            ],
        ),
        migrations.CreateModel(
            name='InspeccionDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observaciones', models.CharField(max_length=1000)),
                ('imagen', models.ImageField(upload_to='')),
                ('status', models.CharField(choices=[('OK', 'CORRECTO'), ('BA', 'AVERIA')], max_length=2)),
                ('es_llanta', models.BooleanField()),
                ('id_elemento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.Elemento')),
                ('id_inspeccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.Inspeccion')),
            ],
        ),
        migrations.CreateModel(
            name='Llantas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dot_tracking_num', models.CharField(max_length=12)),
                ('fecha_alta', models.DateTimeField()),
                ('fecha_baja', models.DateTimeField()),
                ('Presion_max', models.CharField(max_length=12)),
                ('numero_serie', models.CharField(max_length=20)),
                ('fabricante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.Fabricante')),
            ],
        ),
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('ap_paterno', models.CharField(max_length=100)),
                ('ap_materno', models.CharField(max_length=100)),
                ('telefono_particular', models.CharField(max_length=10)),
                ('telefono_celular', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('fecha_alta', models.DateTimeField()),
                ('fecha_baja', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='OperadorEvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField()),
                ('Fecha_terminal', models.DateTimeField()),
                ('Comentario_extendido', models.CharField(max_length=500)),
                ('id_operador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.Operador')),
            ],
        ),
        migrations.CreateModel(
            name='StatusDeOperador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TipoUnidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TipoVisa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_tractor', models.CharField(max_length=12)),
                ('placas', models.CharField(max_length=12)),
                ('id_tipounidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.TipoUnidad')),
            ],
        ),
        migrations.AddField(
            model_name='operadorevento',
            name='id_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.StatusDeOperador'),
        ),
        migrations.AddField(
            model_name='operador',
            name='id_tipovisa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.TipoVisa'),
        ),
        migrations.AddField(
            model_name='operador',
            name='status_operador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.StatusDeOperador'),
        ),
        migrations.AddField(
            model_name='inspeccion',
            name='id_tractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.Unidad'),
        ),
        migrations.AddField(
            model_name='inpeccionllantas',
            name='id_inspecciondetalle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.InspeccionDetalle'),
        ),
        migrations.AddField(
            model_name='inpeccionllantas',
            name='id_llanta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.Llantas'),
        ),
        migrations.AddField(
            model_name='caja',
            name='id_capacidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.Capacidad'),
        ),
        migrations.AddField(
            model_name='caja',
            name='id_faricante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sds.Fabricante'),
        ),
    ]
