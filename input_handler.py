import re

from utils import camel_to_kebab


def parse_fields(fields):
	parsed_fields = []
	for field in fields:
		# Initialize dictionary to hold parsed elements for each field
		field_dict = {}

		# Extract type and name
		type_name = field.split('-')[0]
		attr_name = field.split('-')[1].split('[')[0].split('{')[0]
		field_dict['type'] = type_name.strip()
		field_dict['name'] = attr_name.strip()

		# Extract column name if exists
		match_column = re.search(r'\[(.*?)\]', field)
		field_dict['column_name'] = match_column.group(1).strip() if match_column else None

		# Extract join details if exists
		match_join = re.search(r'\{(.*?)\}', field)
		field_dict['join_details'] = match_join.group(1).strip() if match_join else None

		parsed_fields.append(field_dict)
	return parsed_fields

def gather_inputs(input_function=input):
	# Gather user inputs
	group_name = input_function("Enter the group project name (dots-separated): ")
	entity_name = input_function("Enter the entity name (pascal case): ")
	language = input_function("Enter the language (US/BR): ")
	fields_input = input_function("Enter the fields (semicolon-separated): ")
	table_name = input_function("Enter the table name (database table name, using snake case): ")
	table_schema = input_function("Enter the table schema: ")
	jdk_version = input_function("Enter JDK version (11/17): ")
	fields = fields_input.split(';')

	# group_name = "com.example"
	# entity_name = "personHistory"
	# language = "US"
	# fields_input = "String-firstName[first_name];Long-age;Date-birthDate;Long-addressName[address];History-history[seq_history]{n-1,seq_history}"
	# table_name = "person_table"
	# table_schema = "public"
	# jdk_version = "11"
	# fields = fields_input.split(';')

	return {
		'group_name': group_name.strip(),
		'entity_name': entity_name.strip(),
		'language': language.strip(),
		'fields_input': parse_fields(fields),
		'table_name': table_name.strip(),
		'table_schema': table_schema.strip(),
		'jdk_version': jdk_version.strip(),
	}
