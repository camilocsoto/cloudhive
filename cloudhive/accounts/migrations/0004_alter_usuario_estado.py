# Generated by Django 5.2 on 2025-04-16 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_usuario_estado_alter_usuario_rol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='estado',
            field=models.IntegerField(choices=[(0, 'inactivo'), (1, 'activo')], default=1),
        ),
    ]
