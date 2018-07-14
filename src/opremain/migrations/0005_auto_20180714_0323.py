# Generated by Django 2.0.7 on 2018-07-13 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opremain', '0004_auto_20180712_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='title',
            field=models.SlugField(blank=True, null=True, verbose_name='설정제목'),
        ),
        migrations.AlterField(
            model_name='config',
            name='extra_columns',
            field=models.CharField(max_length=255, verbose_name='표기할컬럼'),
        ),
    ]