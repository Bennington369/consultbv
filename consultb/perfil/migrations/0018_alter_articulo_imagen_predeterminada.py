# Generated by Django 4.0.3 on 2023-04-15 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0017_notificacion_user_to_alter_notificacion_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='imagen_predeterminada',
            field=models.ImageField(default='perfiles/shop.png', upload_to='articulos'),
        ),
    ]