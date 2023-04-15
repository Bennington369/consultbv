# Generated by Django 4.0.3 on 2023-04-13 17:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0014_producto_creat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='creat',
            new_name='create',
        ),
        migrations.AddField(
            model_name='categoria',
            name='create',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
