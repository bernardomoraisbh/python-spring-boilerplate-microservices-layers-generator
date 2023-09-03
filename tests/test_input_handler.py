import sys
import unittest
from unittest.mock import patch

sys.path.append("..")

from input_handler import gather_inputs


class TestInputHandlerUS(unittest.TestCase):

	@patch('builtins.input', side_effect=['v1', 'com.example', 'Person', 'US', 'person_table', 'public', '11', 'String-firstName[first_name];Long-age;Date-birthDate;Long-addressName[address];History-history[seq_history]{n-1,seq_history}'])
	def test_gather_inputs(self, mock_input):
		self.maxDiff = None
		expected_output = {
			'group_name': 'com.example',
			'entity_name': 'Person',
			'language': 'US',
			'fields_input': [
				{'type': 'String', 'name': 'firstName', 'column_name': 'first_name', 'join_details': None},
				{'type': 'Long', 'name': 'age', 'column_name': None, 'join_details': None},
				{'type': 'Date', 'name': 'birthDate', 'column_name': None, 'join_details': None},
				{'type': 'Long', 'name': 'addressName', 'column_name': 'address', 'join_details': None},
				{'type': 'History', 'name': 'history', 'column_name': 'seq_history', 'join_details': 'n-1,seq_history'}
			],
			'table_name': 'person_table',
			'table_schema': 'public',
			'jdk_version': '11'
		}
		self.assertEqual(gather_inputs(input_function=mock_input), expected_output)

	@patch('builtins.input', side_effect=['  v1  ', '  com.example  ', '  Person  ', '  US  ', '  person_table  ', '  public  ', '  11  ', '  String-firstName[first_name]  ;  Long-age;Date-birthDate;Long-addressName[address];History-history[seq_history]{n-1,seq_history}  '])
	def test_gather_inputs_with_extra_spaces(self, mock_input):
		self.maxDiff = None
		# This expected_output is similar to the first one; the function should be able to handle extra spaces.
		expected_output = {
			'group_name': 'com.example',
			'entity_name': 'Person',
			'language': 'US',
			'fields_input': [
				{'type': 'String', 'name': 'firstName', 'column_name': 'first_name', 'join_details': None},
				{'type': 'Long', 'name': 'age', 'column_name': None, 'join_details': None},
				{'type': 'Date', 'name': 'birthDate', 'column_name': None, 'join_details': None},
				{'type': 'Long', 'name': 'addressName', 'column_name': 'address', 'join_details': None},
				{'type': 'History', 'name': 'history', 'column_name': 'seq_history', 'join_details': 'n-1,seq_history'}
			],
			'table_name': 'person_table',
			'table_schema': 'public',
			'jdk_version': '11'
		}
		self.assertEqual(gather_inputs(input_function=mock_input), expected_output)

class TestInputHandlerBR(unittest.TestCase):

	@patch('builtins.input', side_effect=['v1', 'com.example', 'Person', 'BR', 'person_table', 'public', '11', 'String-firstName[first_name];Long-age;Date-birthDate;Long-addressName[address];History-history[seq_history]{n-1,seq_history}'])
	def test_gather_inputs(self, mock_input):
		self.maxDiff = None
		expected_output = {
			'group_name': 'com.example',
			'entity_name': 'Person',
			'language': 'BR',
			'fields_input': [
				{'type': 'String', 'name': 'firstName', 'column_name': 'first_name', 'join_details': None},
				{'type': 'Long', 'name': 'age', 'column_name': None, 'join_details': None},
				{'type': 'Date', 'name': 'birthDate', 'column_name': None, 'join_details': None},
				{'type': 'Long', 'name': 'addressName', 'column_name': 'address', 'join_details': None},
				{'type': 'History', 'name': 'history', 'column_name': 'seq_history', 'join_details': 'n-1,seq_history'}
			],
			'table_name': 'person_table',
			'table_schema': 'public',
			'jdk_version': '11'
		}
		self.assertEqual(gather_inputs(input_function=mock_input), expected_output)

	@patch('builtins.input', side_effect=['  v1  ', '  com.example  ', '  Person  ', '  BR  ', '  person_table  ', '  public  ', '  11  ', '  String-firstName[first_name]  ;  Long-age;Date-birthDate;Long-addressName[address];History-history[seq_history]{n-1,seq_history}  '])
	def test_gather_inputs_with_extra_spaces(self, mock_input):
		self.maxDiff = None
		# This expected_output is similar to the first one; the function should be able to handle extra spaces.
		expected_output = {
			'group_name': 'com.example',
			'entity_name': 'Person',
			'language': 'BR',
			'fields_input': [
				{'type': 'String', 'name': 'firstName', 'column_name': 'first_name', 'join_details': None},
				{'type': 'Long', 'name': 'age', 'column_name': None, 'join_details': None},
				{'type': 'Date', 'name': 'birthDate', 'column_name': None, 'join_details': None},
				{'type': 'Long', 'name': 'addressName', 'column_name': 'address', 'join_details': None},
				{'type': 'History', 'name': 'history', 'column_name': 'seq_history', 'join_details': 'n-1,seq_history'}
			],
			'table_name': 'person_table',
			'table_schema': 'public',
			'jdk_version': '11'
		}
		self.assertEqual(gather_inputs(input_function=mock_input), expected_output)

if __name__ == '__main__':
	unittest.main()
