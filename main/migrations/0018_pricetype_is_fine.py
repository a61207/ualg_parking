# Generated by Django 4.0.6 on 2022-07-06 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_contrato_criadoem_alter_contrato_editadoem'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricetype',
            name='is_fine',
            field=models.BooleanField(db_column='IsFine', default=False, verbose_name='Is Fine'),
        ),
    ]
