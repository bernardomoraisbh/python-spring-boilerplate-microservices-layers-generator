import sys
import unittest
from unittest.mock import patch

sys.path.append("..")

from code_generators.entity_generator import EntityGenerator
from language_dictionary import LocalizationDict


class TestEntityGenerator(unittest.TestCase):

	def setUp(self):
		self.entity_generator = EntityGenerator(
			group_name='com.example',
			entity_name='personHistory',
			language_dict=LocalizationDict('US'),
			fields_input=[
				{'type': 'String', 'name': 'firstName', 'column_name': 'first_name', 'join_details': None},
				{'type': 'Long', 'name': 'age', 'column_name': None, 'join_details': None},
				{'type': 'Date', 'name': 'birthDate', 'column_name': None, 'join_details': None},
				{'type': 'Long', 'name': 'addressName', 'column_name': 'address', 'join_details': None},
				{'type': 'History', 'name': 'history', 'column_name': 'seq_history', 'join_details': 'n-1,seq_history'}
			],
			table_name='person_table',
			table_schema='public',
			jdk_version='11',
			complete_package_path='src/main/java/com/example'
		)

	@patch('code_generators.entity_generator.EntityGenerator.write_to_java_file')
	def test_generate(self, mock_write_to_java_file):
		self.entity_generator.generate()
		mock_write_to_java_file.assert_called()  # Verifies that write_to_java_file was called

	def test_generate_field_code(self):
		actual_output = self.entity_generator.generate_field_code()
		# print("Actual Output:")
		# print(actual_output)
		# print("Expected Output:")
		expected_output = '''
		@Column(name = "first_name")
						private String firstName;

						@Column(name = "age")
						private Long age;

						@Column(name = "birth_date")
						@Temporal(TemporalType.TIMESTAMP)
						private Date birthDate;

						@Column(name = "address")
						private Long addressName;

						@ManyToOne(fetch = FetchType.LAZY)
						@JoinColumn(name = "seq_history")
						@Column(name = "seq_history")
						private History history;
		'''.strip()
		# print(expected_output)
		self.assertEqual(actual_output, expected_output)

	def test_temporal_annotation(self):
		self.assertEqual(self.entity_generator.temporal_annotation("birthdayDate"), '@Temporal(TemporalType.TIMESTAMP)')
		self.assertEqual(self.entity_generator.temporal_annotation("name"), '')

if __name__ == '__main__':
	unittest.main()
