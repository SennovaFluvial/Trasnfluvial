# Generated by Django 3.1.2 on 2020-11-14 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20201114_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.dependencia'),
        ),
    ]