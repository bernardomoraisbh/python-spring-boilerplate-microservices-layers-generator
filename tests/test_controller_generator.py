import sys
import unittest
from unittest.mock import patch

sys.path.append("..")

from code_generators.controller_generator import ControllerGenerator  # adjust this import based on your package structure
from language_dictionary import LocalizationDict


class TestControllerGeneratorBR(unittest.TestCase):

	def setUp(self):
		self.controller_generator = ControllerGenerator(
			group_name='com.example',
			entity_name='Person',
			language_dict=LocalizationDict('US'),
			fields_input=[
					{'type': 'String', 'name': 'firstName'},
					{'type': 'Long', 'name': 'age'},
					{'type': 'Date', 'name': 'birthDate'}
			],
			table_name='person_table',
			table_schema='public',
			jdk_version='11',
			complete_package_path='src/main/java/com/example'
		)

	@patch('code_generators.controller_generator.ControllerGenerator.write_to_java_file')
	def test_generate(self, mock_write_to_java_file):
		self.controller_generator.generate()
		mock_write_to_java_file.assert_called()

class TestControllerGeneratorUS(unittest.TestCase):

	def setUp(self):
		self.controller_generator = ControllerGenerator(
			group_name='com.example',
			entity_name='Person',
			language_dict=LocalizationDict('BR'),
			fields_input=[
				{'type': 'String', 'name': 'firstName'},
				{'type': 'Long', 'name': 'age'},
				{'type': 'Date', 'name': 'birthDate'}
			],
			table_name='person_table',
			table_schema='public',
			jdk_version='11',
			complete_package_path='src/main/java/com/example'
		)

	@patch('code_generators.controller_generator.ControllerGenerator.write_to_java_file')
	def test_generate(self, mock_write_to_java_file):
		self.controller_generator.generate()
		mock_write_to_java_file.assert_called()

if __name__ == '__main__':
	unittest.main()
