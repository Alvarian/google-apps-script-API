from flask import json
from scripts.globals import get_col_pos_by_name
import gender_guesser.detector as gender


def genderize(name, data):
	d = gender.Detector()

	def determine_header(old_headers):
		if 'gender' in old_headers:
			return old_headers
		else:
			old_headers.append('gender')
			return old_headers

	headers = determine_header(data[0])	
	firstN_pos = get_col_pos_by_name(headers, name)
	
	for i in range(1, len(data)):
		row = data[i]
		first_name = row[firstN_pos]

		new_gender = d.get_gender(first_name)
		row.append(new_gender)

	payload = json.dumps(data)

	return payload

def slice_middle_name(columns, data):
	return 'slice'

def format_address(columns, data):
	return 'format'

def get_duplicates(columns, data):
	return 'get'

def del_duplicates(columns, data):
	return 'del'
