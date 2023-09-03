import sys
import unittest
from unittest.mock import patch

sys.path.append("..")

from code_generators.service_generator import ServiceGenerator  # adjust this import based on your package structure


class TestServiceGeneratorUS(unittest.TestCase):

	def setUp(self):
		self.service_generator = ServiceGenerator(
			group_name='com.example',
			entity_name='Person',
			language='US',
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

	@patch('code_generators.service_generator.ServiceGenerator.write_to_java_file')
	def test_generate(self, mock_write_to_java_file):
		self.service_generator.generate()
		mock_write_to_java_file.assert_called()

class TestServiceGeneratorBR(unittest.TestCase):

	def setUp(self):
		self.service_generator = ServiceGenerator(
			group_name='com.example',
			entity_name='Person',
			language='BR',
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

	@patch('code_generators.service_generator.ServiceGenerator.write_to_java_file')
	def test_generate(self, mock_write_to_java_file):
		self.service_generator.generate()
		mock_write_to_java_file.assert_called()

if __name__ == '__main__':
	unittest.main()
