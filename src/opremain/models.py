import os

from django.db import models
from django.conf import settings
from django.urls import reverse


class Narcotic(models.Model):
    narcotic_name = models.CharField('약품명', max_length=50, unique=True)
    edi_code = models.CharField('보험코드', max_length=20)
    price = models.IntegerField('가격', default=0)
    narcotic_class = models.CharField('마약류구분', max_length=5, choices=[('향정', '향정'), ('마약', '마약')])
    shape = models.CharField('제형', max_length=10, choices=[('VIAL', 'VIAL'), ('AMP', 'AMP')])
    keyword = models.CharField('키워드', max_length=50)
    sub_keyword = models.CharField('보조키워드', max_length=50, blank=True, null=True)
    company_keyword = models.CharField('판매사', max_length=50, blank=True, null=True)
    full_amt_exp = models.CharField('전체함량표기', max_length=50)
    amt_volum_exp = models.CharField('ml표기', max_length=50, blank=True, null=True)
    amt_weight_exp = models.CharField('mg표기', max_length=50, blank=True, null=True)
    pct_exp = models.CharField('퍼센트표기', max_length=50, blank=True, null=True)
    amt_ml = models.IntegerField('ml함량', blank=True, null=True)
    amt_mg = models.IntegerField('mg함량', blank=True, null=True)
    unit = models.CharField('주함량단위', max_length=10, choices=[('ml', 'ml'), ('mg', 'mg'), ('g', 'g')])
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '마약류'
        verbose_name_plural = '마약류'

    def __str__(self):
        return self.narcotic_name


class Config(models.Model):
    title = models.CharField('설정제목', max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key_column = models.CharField('약품명컬럼명', max_length=50)
    not_null_columns = models.CharField('필수컬럼', max_length=50, blank=True, null=True)
    order_amt_column = models.CharField('처방량(소수점단위)컬럼명', max_length=50)
    extra_columns = models.TextField('표기할컬럼(순서)', blank=True, null=True)
    orderby_columns = models.CharField('정렬기준컬럼', max_length=255, blank=True, null=True)
    activated = models.BooleanField('사용중', default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '설정'
        verbose_name_plural = '설정'

    def __str__(self):
        return "/".join(filter(None, [self.title, self.user.username]))

    def save(self, *args, **kwargs):
        self.__class__.objects.filter(user=self.user).update(activated=False)
        return super(Config, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('opremain:config-detail', kwargs={'pk': self.pk})
    
    def get_valid_namemap_set(self):
        return self.namemap_set.filter(excepted=False, activated=True)

    def get_excepted_namemap_set(self):
        return self.namemap_set.filter(excepted=True, activated=True)
    
    


class NameMap(models.Model):
    config = models.ForeignKey(Config, on_delete=models.CASCADE)
    current_name = models.CharField('사용중인이름', max_length=255)
    mapping_to = models.ForeignKey(Narcotic, on_delete=models.CASCADE, null=True, blank=True)
    excepted = models.BooleanField('집계제외', default=False)
    activated = models.BooleanField('사용중', default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '약품명매칭'
        verbose_name_plural = '약품명매칭'
    
    def __str__(self):
        return self.current_name
    
    def save(self, **kwargs):
        if not self.excepted and not self.mapping_to:
            self.activated = False
        return super().save(**kwargs)


UPLOAD_DIR = 'opremain'

class NarcoticUseFile(models.Model):
    config = models.ForeignKey(Config, on_delete=models.CASCADE)
    excel = models.FileField('엑셀파일', upload_to=UPLOAD_DIR)
    description = models.CharField('파일명', max_length=50, blank=True, null=True)
    updated = models.DateTimeField('생성일', auto_now=True)
    created = models.DateTimeField('생성일', auto_now_add=True)

    class Meta:
        verbose_name = '마약류불출내역'
        verbose_name_plural = '마약류불출내역'
        ordering = '-created',
    
    def __str__(self):
        return self.description
    
    def save(self, **kwargs):
        if not self.id:
            self.description = os.path.basename(self.excel.file.name)
        super().save(**kwargs)
    
    

    