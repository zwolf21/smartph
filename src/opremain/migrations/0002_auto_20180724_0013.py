# Generated by Django 2.0.7 on 2018-07-23 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opremain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='namemap',
            name='mapping_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='opremain.Narcotic'),
        ),
    ]
