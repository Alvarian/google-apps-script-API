from flask import Flask, request

app = Flask(__name__)
from scripts.scripts import genderize, slice_middle_name, format_address, get_duplicates, del_duplicates


@app.route('/api/v1/genderize', methods=['post'])
def get_new_genders():
	payload = request.get_json()
	
	return genderize(payload['columns'], payload['data'])

@app.route('/api/v1/sliceMiddle', methods=['post'])
def get_middle_names():
	payload = request.get_json()

	return slice_middle_name(payload['columns'], payload['data'])

@app.route('/api/v1/formatAdd', methods=['post'])
def get_addresses():
	return format_address()

@app.route('/api/v1/getDupes', methods=['post'])
def get_dupes():
	return get_duplicates()

@app.route('/api/v1/delDupes', methods=['post'])
def del_dupes():
	return del_duplicates()


if __name__ == '__main__':
	app.run(debug=True)