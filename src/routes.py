from flask import Flask, request, jsonify
import os

from src import app
from src.scripts import genderize, slice_middle_name, format_address, get_duplicates, del_duplicates


@app.route('/api/v1/genderize', methods=['post'])
def get():
	return genderize()

@app.route('/api/v1/sliceMiddle', methods=['post'])
def get():
	return slice_middle_name()

@app.route('/api/v1/formatAdd', methods=['post'])
def get():
	return format_address()

@app.route('/api/v1/getDupes', methods=['post'])
def get():
	return get_duplicates()

@app.route('/api/v1/delDupes', methods=['post'])
def get():
	return del_duplicates()
