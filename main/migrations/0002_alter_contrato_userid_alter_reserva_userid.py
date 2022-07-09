# Generated by Django 4.0.6 on 2022-07-09 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='userid',
            field=models.ForeignKey(db_column='ClientID', on_delete=django.db.models.deletion.CASCADE, to='main.client'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='userid',
            field=models.ForeignKey(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, to='main.client'),
        ),
    ]
