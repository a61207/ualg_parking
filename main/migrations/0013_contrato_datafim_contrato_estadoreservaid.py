# Generated by Django 4.0.4 on 2022-07-05 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_contrato_parqueid_remove_contrato_zonaid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='datafim',
            field=models.DateField(blank=True, db_column='DataFim', null=True),
        ),
        migrations.AddField(
            model_name='contrato',
            name='estadoreservaid',
            field=models.ForeignKey(db_column='EstadoReservaID', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='main.estadoreserva'),
        ),
    ]
