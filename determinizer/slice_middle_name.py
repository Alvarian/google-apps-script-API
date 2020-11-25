from flask import json
from determinizer.globals import get_col_pos_by_name, determine_headers, search_list_for_upper
import re, string


def slice_middle_name(columns, data):
	firstN_col = columns[0]
	lastN_col = columns[1]

	headers = determine_headers(data[0], 'Middle Name')	
	middleN_pos = get_col_pos_by_name(headers, 'Middle Name')

	def split_from_last_name():
		lastN_pos = get_col_pos_by_name(headers, lastN_col)
		weird_rows = []
		empty_rows = []

		for i in range(1, len(data)):
			row = data[i]
			last_name = row[lastN_pos]

			if re.search("(^st\.|^o'|^saint\.|^d')", last_name.lower()):
				parts = re.split("\s", last_name)

				if len(parts) > 2:
					weird_rows.append(row)
				elif len(parts) == 2:
					if re.search("(^st\.$|^o'$|^saint\.$|^d'$)", parts[0].lower()):
						row[lastN_pos] = parts[0].title() + " " + parts[1].title()
					else:
						row[middleN_pos] = parts[0].title()
						row[lastN_pos] = parts[1].title()
				else:
					row[lastN_pos] = last_name
			elif re.search("(esq\.$|esq$|III$|jr$|jr\.$)", last_name.lower()):
				parts = re.split("\s", last_name)

				if len(parts) > 2:
					weird_rows.append(row)
					row[middleN_pos] = parts[0].title()

					new_last_name = ''
					for i in range(1, len(parts)):
						if i < len(parts):
							new_last_name = new_last_name + parts[i] + " "
						else:
							new_last_name = new_last_name + parts[i]

					row[lastN_pos] = new_last_name
				elif len(parts) == 2:
					if re.search("(^esq\.$|^esq$|^III$|^jr$|^jr\.$)", parts[1].lower()):
						row[lastN_pos] = parts[0].title() + " " + parts[1].title()
					else:
						row[middleN_pos] = parts[0].title()
						row[lastN_pos] = parts[1].title()				
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

	def split_from_first_name():
		lastN_payload = json.loads(split_from_last_name())
		firstN_pos = get_col_pos_by_name(headers, firstN_col)

		for row in lastN_payload['data']:
			first_name = row[firstN_pos]

			if not row[middleN_pos]:
				if re.search("('|\.)", first_name.lower()):
					parts = re.split("\s", first_name)

					if len(parts) > 2:
						lastN_payload['weird'].append(row)
					elif len(parts) == 2:
						row[firstN_pos] = parts[0].title()
						row[middleN_pos] = parts[1].title()
					else:
						row[firstN_pos] = parts[0].title()
				else:
					if not first_name:
						lastN_payload['empty'].append(row)
					else:
						parts = re.split("\s|\W", first_name)

						if len(parts) > 2:
							lastN_payload['weird'].append(row)
						elif len(parts) == 2:
							row[firstN_pos] = parts[0].title()
							row[middleN_pos] = parts[1].title()
						else:
							row[firstN_pos] = parts[0].title()

		payload = json.dumps({
			"weird": lastN_payload['weird'],
			"empty": lastN_payload['empty'],
			"data": lastN_payload['data']
		})

		return payload
	
	return split_from_first_name()	
