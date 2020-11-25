from flask import json
from scripts.globals import get_col_pos_by_name, determine_headers, search_list_for_upper
import gender_guesser.detector as gender
import re
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
		for row in data:
			last_name = row[lastN_pos]

			if re.search("(^St\.|^st\.|^O'|^Saint\.|^saint\.|D'|d')", last_name):
				parts = re.split("\s", last_name)
				print("suppose to be protected", parts)
			elif re.search("esq.$|Esq.$|esq$|Esq$|III|jr|jr.", last_name):
				parts = re.split("\s", last_name)
				print("suppose to be protected 2", parts)
			else:
				parts = re.split("\s|\W", last_name)

				adjective_or_whole = parts[0]
				if type(adjective_or_whole) == str:
					if len(parts) > 2:
						print(parts, )
					elif len(parts) == 2:
						if re.search("^Mc$|^mc$|^Du$|^du$|^Mac$|^mac$", adjective_or_whole):
							row[lastN_pos] = parts[0]+parts[1]
							print("suppose to be fused", parts)
						else:
							row[middleN_pos] = parts[0]
							row[lastN_pos] = parts[1]
					else:
						if re.search("^von|^Von|^van|^Van|^saint|^Saint|^St|^st|^De|^de|^La|^la|^Lo|^lo|^Di|^di", last_name) and bool(search_list_for_upper(last_name)):
							# print(adjective_or_whole, parts, last_name)
							print("suppose to be separate", last_name)

		return
	
	# def format_apostrophe_into_last_name():
	# 	return

	def split_from_first_name():
		return

	# def format_apostrophe_into_first_name():
	# 	return

	split_from_last_name()	
	return 'slice'

def format_address(columns, data):
	return 'format'

def get_duplicates(columns, data):
	return 'get'

def del_duplicates(columns, data):
	return 'del'
