def get_col_pos_by_name(columns, name):
	for index in range(len(columns)):
		if columns[index] == name:
			return index