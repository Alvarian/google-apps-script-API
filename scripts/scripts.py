from flask import json
from scripts.globals import get_col_pos_by_name, determine_headers, search_list_for_upper
import gender_guesser.detector as gender
import re, string
# print(bool(search_list_for_upper("Saint-Fort")))
# print(bool(re.search("^von|^Von|^van|^Van|^saint|^Saint|^St|^st|^De|^de|^La|^la|^Lo|^lo|^Di|^di", "Saint-Fort")))
# print(re.search("^von|^Von|^van|^Van|^saint|^Saint|^St|^st|^De|^de|^La|^la|^Lo|^lo|^Di|^di", "Saint-Fort") and bool(search_list_for_upper("Saint-Fort")))


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

def slice_middle_name(columns, data):
	firstN_col = columns[0]
	lastN_col = columns[1]

	headers = determine_headers(data[0], 'Middle Name')	
	firstN_pos = get_col_pos_by_name(headers, firstN_col)
	middleN_pos = get_col_pos_by_name(headers, 'Middle Name')
	lastN_pos = get_col_pos_by_name(headers, lastN_col)

	def split_from_last_name():
		weird_rows = []
		empty_rows = []

		for i in range(1, len(data)):
			row = data[i]
			last_name = row[lastN_pos]

			if re.search("(^st\.|^o'|^saint\.|d')", last_name.lower()):
				parts = re.split("\s", last_name)

				if len(parts) > 2:
					weird_rows.append(row)
				elif len(parts) == 2:
					row[lastN_pos] = string.capwords(parts[0] + " " + parts[1])
				else:
					row[lastN_pos] = string.capwords(last_name)
			elif re.search("esq.$|esq$|III|jr|jr.", last_name.lower()):
				parts = re.split("\s", last_name)
				print("suppose to be protected 2", parts)
			else:
				parts = re.split("\s|\W", last_name)

				adjective_or_whole = parts[0]
				if type(adjective_or_whole) == str:
					if len(parts) > 2:
						weird_rows.append(row)
					elif len(parts) == 2:
						if re.search("^mc$|^du$|^di$|^mac$", adjective_or_whole.lower()):
							row[lastN_pos] = string.capwords(parts[0]) + string.capwords(parts[1])
						elif re.search("^saint$|^st$", adjective_or_whole.lower()):
							row[lastN_pos] = string.capwords(last_name)
						elif re.search("^von$|^van$|^de$|^la$|^lo$", adjective_or_whole.lower()):
							row[lastN_pos] = adjective_or_whole.lower() + " " + string.capwords(parts[1])
						else:
							row[middleN_pos] = string.capwords(parts[0])
							row[lastN_pos] = string.capwords(parts[1])
					elif len(parts) == 1:
						if bool(search_list_for_upper(last_name)) and re.search("^von|^van|^saint|^st|^de|^la|^lo", last_name.lower()):
							index = search_list_for_upper(last_name)['index']

							row[lastN_pos] = last_name[0:index] + " " + last_name[index:len(last_name)]
						else:
							row[lastN_pos] = string.capwords(last_name)
					else:
						empty_rows.append(row)

		payload = json.dumps({
			"weird": weird_rows,
			"empty": empty_rows,
			"data": data
		})

		return payload
	
	# def format_apostrophe_into_last_name():
	# 	return

	def split_from_first_name():
		return

	# def format_apostrophe_into_first_name():
	# 	return
	
	return split_from_last_name()	

def format_address(columns, data):
	return 'format'

def get_duplicates(columns, data):
	return 'get'

def del_duplicates(columns, data):
	return 'del'
