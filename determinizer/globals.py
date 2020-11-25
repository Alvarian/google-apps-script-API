def get_col_pos_by_name(columns, name):
	for index in range(len(columns)):
		if columns[index] == name:
			return index

def determine_headers(old_headers, header):
	if header in old_headers:
		return old_headers
	else:
		old_headers.append(header)
		return old_headers

def search_list_for_upper(word):
	upper_check = [it.upper() for it in word]
	
	for i in range(1, len(word)):
		if word[i] in upper_check:
			# print(word[i], word[i] in upper_check)
			payload = {
				"has_upper": word[i] in upper_check,
				"letter": word[i],
				"index": i
			}

			return payload

	return False