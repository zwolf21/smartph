import functools, re
from mimetypes import guess_type
from urllib.parse import quote

from django.utils.text import slugify
from django.http import HttpResponse


# 파일 리스폰스, 한글로 파일 이름 지정 가능
def file_response(content, filename):
	ctype, encoding = guess_type(filename)
	response = HttpResponse(content, content_type=ctype or 'applicatioin/octet-stream')
	if encoding:
		response['Content-Encoding'] = encoding
	response['Content-Disposition'] = "attachment; filename*=UTF-8''{}".format(quote(filename.encode('utf-8')))
	return response


def unique_slugify(instance, field_to_slugify, slug_field_name='slug', post_fix_init=1, **kwargs):
	model = instance.__class__
	counter = post_fix_init
	value_to_slugify = getattr(instance, field_to_slugify)
	slug = slugify(value_to_slugify, **kwargs)
	ret = slug
	while True:
		if model.objects.filter(**{slug_field_name: ret}).exists():
			ret = "{}-{}".format(slug, counter)
			counter +=1 			
		else:
			return ret

# 20171011-002 형식으로 슬러그화
def sequence_date_slugify(instance, datefield_to_slugify, num_digit=3):
	model = instance.__class__
	date = getattr(instance, datefield_to_slugify)
	str_date = date.strftime("%Y%m%d")
	format_string = "{}-" + "{:0" + str(num_digit) + "d}"
	seq = 1
	while True:
		slug = format_string.format(str_date, seq)
		if model.objects.filter(slug=slug).exists():
			seq +=1
			continue
		return slug


def sequence_fk_slugify(instance, fk_field_to_slugify, fk_lookup_field, slug_field_name='slug', post_fix_init=1):
	model = instance.__class__
	parent = getattr(instance, fk_field_to_slugify)
	str_parent = getattr(parent, fk_lookup_field)
	seq = post_fix_init
	while True:
		slug = "{}-{}".format(str_parent, seq)
		if model.objects.filter(**{slug_field_name: slug}).exists():
			seq+=1
			continue
		return slug


def csv2array(csv, must_haveset=None):
	if csv:
		ret = re.split('[\s,]+', csv)
		if must_haveset is not None:
			return [item for item in ret if item in must_haveset]
		else: 
			return list(filter(None, ret))
	return []


def classinit(attrs):
    def wrapper(cls):
        for key, val in attrs.items():
            setattr(cls, key, val)
        return cls
    return wrapper


def findsim(value: str, arr: list):
	matched = []
	value = value.strip()
	arr = map(str.strip, arr)
	for item in arr:
		if not isinstance(item, str):
			continue
		if item == value:
			return item
		elif value in item or item in value:
			matched.append(item)
	
	if len(matched) == 0:
		return None
	else:
		return min(matched, key=len)
