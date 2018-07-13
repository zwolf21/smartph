import os

def is_excel(excel):
	fn, ext = os.path.splitext(excel)
	if ext in ['.xls', '.xlsx']:
		return True
	return False
