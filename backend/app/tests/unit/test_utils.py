from app.utils import APPLICATION_REQUIRED_FIELDS, review_information_received, parse_datetime_to_str, compare_required_fields
from datetime import datetime


def test_review_information_received():
	test_data = {
		'name': {
			'value': 'Harry',
			'expected_response': True
		},
		'last_name': {
			'value': 'Potter 1',
			'expected_response': False
		},
		'identification': {
			'value': '1234567890',
			'expected_response': True
		},
		'age': {
			'value': 123,
			'expected_response': False
		},
		'magic_affinity': {
			'value': 'water',
			'expected_response': True
		}
	}
	for key in test_data:
		res = review_information_received(test_data[key]['value'],APPLICATION_REQUIRED_FIELDS[key]['regex'])
		assert res == test_data[key]['expected_response']

def test_parse_datetime_to_str():
	current_time = datetime.now()
	test_parse = parse_datetime_to_str(current_time)
	assert type(test_parse) == str

def test_compare_required_fields():
	test_data = {
		'name': {
			'value': 'Harry',
		},
		'last_name': {
			'value': 'Potter'
		},
		'identification': {
			'value': '1234567890'
		},
		'age': {
			'value': 17
		}
	}
	res = compare_required_fields(test_data, APPLICATION_REQUIRED_FIELDS)
	assert res == True