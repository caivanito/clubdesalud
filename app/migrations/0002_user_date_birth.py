# Generated by Django 3.2.4 on 2021-08-03 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_birth',
            field=models.DateField(null=True, verbose_name='Fecha de Nacimiento'),
        ),
    ]