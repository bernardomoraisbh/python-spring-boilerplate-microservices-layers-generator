import sys
import unittest
from unittest.mock import patch

sys.path.append("..")

from input_handler import gather_inputs


class TestInputHandler(unittest.TestCase):

	@patch('builtins.input', side_effect=['api.example.test', 'Person', 'US', 'String-firstName;Long-age', 'person_table', 'public', '11'])
	def test_gather_inputs(self, mock_input):
		expected_output = {
			'group_name': 'api.example.test',
			'entity_name': 'Person',
			'language': 'US',
			'fields_input': ['String-firstName', 'Long-age'],
			'table_name': 'person_table',
			'table_schema': 'public',
			'jdk_version': '11'
		}
		self.assertEqual(gather_inputs(input_function=mock_input), expected_output)

	@patch('builtins.input', side_effect=['  api.example.test  ', '  Person  ', '  US  ', '  String-firstName  ;  Long-age  ', '  person_table  ', '  public  ', '  11  '])
	def test_gather_inputs_with_extra_spaces(self, mock_input):
		expected_output = {
			'group_name': 'api.example.test',
			'entity_name': 'Person',
			'language': 'US',
			'fields_input': ['String-firstName', 'Long-age'],
			'table_name': 'person_table',
			'table_schema': 'public',
			'jdk_version': '11'
		}
		self.assertEqual(gather_inputs(input_function=mock_input), expected_output)

if __name__ == '__main__':
	unittest.main()
