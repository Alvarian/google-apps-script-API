from flask import json
from src.globals import get_col_pos_by_name
import gender_guesser.detector as gender


def genderize(name, data):
	d = gender.Detector()
	print(d.get_gender(u"Bob"))
	print(d.get_gender(u"Sally"))
	print(d.get_gender(u"Pauley"))

	headers = data[0]

	col_pos = get_col_pos_by_name(headers, name)

	print(col_pos)

	# return json.dumps(columns)
	return 'Genderized'

def slice_middle_name(columns, data):
	return 'slice'

def format_address(columns, data):
	return 'format'

def get_duplicates(columns, data):
	return 'get'

def del_duplicates(columns, data):
	return 'del'
