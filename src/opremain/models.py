from django.db import models

from django.conf import settings


class Narcotic(models.Model):
    narcotic_name = models.CharField('약품명', max_length=50, unique=True)
    company_name = models.CharField('판매사', max_length=50, blank=True, null=True)
    keyword = models.CharField('키워드', max_length=50)
    sub_keyword = models.CharField('보조키워드', max_length=50, blank=True, null=True)
    full_amt_exp = models.CharField('전체함량표기', max_length=50)
    amt_volum_exp = models.CharField('ml표기', max_length=50, blank=True, null=True)
    amt_weight_exp = models.CharField('mg표기', max_length=50, blank=True, null=True)
    unit = models.CharField('함량단위', max_length=10, choices=[('ml', 'ml'), ('mg', 'mg'), ('g', 'g')])
    amt = models.IntegerField('함량')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


    class Meta:
        verbose_name = '마약류'
        verbose_name_plural = '마약류'

    def __str__(self):
        return self.narcotic_name


class Config(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key_column = models.CharField('약품명컬럼명', max_length=50)
    not_null_columns = models.CharField('필수컬럼', max_length=50, blank=True, null=True)
    order_amt_column = models.CharField('처방량(소수점단위)컬럼명', max_length=50)
    extra_columns = models.CharField('표기할컬럼', max_length=255)
    orderby_columns = models.CharField('정렬기준컬럼', max_length=255, blank=True, null=True)
    activated = models.BooleanField('사용중', default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '설정'
        verbose_name_plural = '설정'

    def __str__(self):
        return "/".join(filter(None, [self.user.username, self.key_column, self.order_amt_column]))


class NameMap(models.Model):
    config = models.ForeignKey(Config, on_delete=models.CASCADE)
    current_name = models.CharField('사용중인이름', max_length=255)
    mapping_to = models.ForeignKey(Narcotic, on_delete=models.CASCADE, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '약품명매칭'
        verbose_name_plural = '약품명매칭'
    
    def __str__(self):
        return self.current_name