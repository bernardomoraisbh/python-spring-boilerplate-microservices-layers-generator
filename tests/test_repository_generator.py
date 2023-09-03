import sys
import unittest
from unittest.mock import patch

sys.path.append("..")

from code_generators.repository_generator import RepositoryGenerator  # adjust this import based on your package structure


class TestRepositoryGeneratorUS(unittest.TestCase):

	def setUp(self):
		self.repo_generator = RepositoryGenerator(
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

	@patch('code_generators.repository_generator.RepositoryGenerator.write_to_java_file')
	def test_base_repository_generator(self, mock_write_to_java_file):
		self.repo_generator.base_repository_generator()
		mock_write_to_java_file.assert_called()

	@patch('code_generators.repository_generator.RepositoryGenerator.write_to_java_file')
	def test_generate(self, mock_write_to_java_file):
		self.repo_generator.generate()
		mock_write_to_java_file.assert_called()

	@patch('code_generators.repository_generator.RepositoryGenerator.write_to_java_file')
	def test_generate_advanced_CRUD_repository(self, mock_write_to_java_file):
		self.repo_generator.generate_advanced_CRUD_repository()
		mock_write_to_java_file.assert_called()


class TestRepositoryGeneratorBR(unittest.TestCase):

	def setUp(self):
		self.repo_generator = RepositoryGenerator(
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

	@patch('code_generators.repository_generator.RepositoryGenerator.write_to_java_file')
	def test_base_repository_generator(self, mock_write_to_java_file):
		self.repo_generator.base_repository_generator()
		mock_write_to_java_file.assert_called()

	@patch('code_generators.repository_generator.RepositoryGenerator.write_to_java_file')
	def test_generate(self, mock_write_to_java_file):
		self.repo_generator.generate()
		mock_write_to_java_file.assert_called()

	@patch('code_generators.repository_generator.RepositoryGenerator.write_to_java_file')
	def test_generate_advanced_CRUD_repository(self, mock_write_to_java_file):
		self.repo_generator.generate_advanced_CRUD_repository()
		mock_write_to_java_file.assert_called()

if __name__ == '__main__':
	unittest.main()
