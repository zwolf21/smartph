# Generated by Django 2.0.7 on 2018-07-23 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='설정제목')),
                ('key_column', models.CharField(max_length=50, verbose_name='약품명컬럼명')),
                ('not_null_columns', models.CharField(blank=True, max_length=50, null=True, verbose_name='필수컬럼')),
                ('order_amt_column', models.CharField(max_length=50, verbose_name='처방량(소수점단위)컬럼명')),
                ('extra_columns', models.TextField(blank=True, null=True, verbose_name='표기할컬럼(순서)')),
                ('orderby_columns', models.CharField(blank=True, max_length=255, null=True, verbose_name='정렬기준컬럼')),
                ('activated', models.BooleanField(default=True, verbose_name='사용중')),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '설정',
                'verbose_name_plural': '설정',
            },
        ),
        migrations.CreateModel(
            name='NameMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_name', models.CharField(max_length=255, verbose_name='사용중인이름')),
                ('excepted', models.BooleanField(default=False, verbose_name='집계제외')),
                ('activated', models.BooleanField(default=False, verbose_name='사용중')),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opremain.Config')),
            ],
            options={
                'verbose_name': '약품명매칭',
                'verbose_name_plural': '약품명매칭',
            },
        ),
        migrations.CreateModel(
            name='Narcotic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('narcotic_name', models.CharField(max_length=50, unique=True, verbose_name='약품명')),
                ('edi_code', models.CharField(max_length=20, verbose_name='보험코드')),
                ('price', models.IntegerField(default=0, verbose_name='가격')),
                ('narcotic_class', models.CharField(choices=[('향정', '향정'), ('마약', '마약')], max_length=5, verbose_name='마약류구분')),
                ('shape', models.CharField(choices=[('VIAL', 'VIAL'), ('AMP', 'AMP')], max_length=10, verbose_name='제형')),
                ('keyword', models.CharField(max_length=50, verbose_name='키워드')),
                ('sub_keyword', models.CharField(blank=True, max_length=50, null=True, verbose_name='보조키워드')),
                ('company_keyword', models.CharField(blank=True, max_length=50, null=True, verbose_name='판매사')),
                ('full_amt_exp', models.CharField(max_length=50, verbose_name='전체함량표기')),
                ('amt_volum_exp', models.CharField(blank=True, max_length=50, null=True, verbose_name='ml표기')),
                ('amt_weight_exp', models.CharField(blank=True, max_length=50, null=True, verbose_name='mg표기')),
                ('pct_exp', models.CharField(blank=True, max_length=50, null=True, verbose_name='퍼센트표기')),
                ('amt_ml', models.IntegerField(blank=True, null=True, verbose_name='ml함량')),
                ('amt_mg', models.IntegerField(blank=True, null=True, verbose_name='mg함량')),
                ('unit', models.CharField(choices=[('ml', 'ml'), ('mg', 'mg'), ('g', 'g')], max_length=10, verbose_name='주함량단위')),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': '마약류',
                'verbose_name_plural': '마약류',
            },
        ),
        migrations.CreateModel(
            name='NarcoticUseFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel', models.FileField(upload_to='opremain', verbose_name='엑셀파일')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='파일명')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='생성일')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opremain.Config')),
            ],
            options={
                'verbose_name': '마약류불출내역',
                'verbose_name_plural': '마약류불출내역',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='namemap',
            name='mapping_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='opremain.Narcotic'),
        ),
    ]
