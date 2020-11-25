from flask import json
from determinizer.globals import get_col_pos_by_name, determine_headers
import gender_guesser.detector as gender

def genderize(columns, data):
	column = columns[0]

	d = gender.Detector()

	headers = determine_headers(data[0], 'gender')	
	firstN_pos = get_col_pos_by_name(headers, column)
	gender_pos = get_col_pos_by_name(headers, 'gender')
	
	for i in range(1, len(data)):
		row = data[i]
		first_name = row[firstN_pos]

		new_gender = d.get_gender(first_name)

		if len(headers) == len(row):
			row[gender_pos] = new_gender
		else:
			row.append(new_gender)

	payload = json.dumps(data)

	return payload