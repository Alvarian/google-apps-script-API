from flask import json
from determinizer.globals import get_col_pos_by_name, determine_headers, search_list_for_upper
import re, string


def get_duplicates(columns, data):
	return 'get'