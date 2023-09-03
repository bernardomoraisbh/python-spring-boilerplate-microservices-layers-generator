import argparse
import re

from gui_input_handler import gather_inputs_gui
from utils import camel_to_snake


def parse_arguments():
	"""Function used to read the execution program args."""
	parser = argparse.ArgumentParser(description="Specify language and input version.")
	parser.add_argument("language", nargs='?', default=None, choices=["US", "BR"], help="Language to use: US or BR")
	parser.add_argument("version", nargs='?', default=None, choices=["v1", "v2", "v3"], help="Input version to use: v1, v2, or v3")
	args = parser.parse_args()
	return args.language, args.version

def parse_fields(fields):
	"""Function used to parse the fields data on the v1 of the script,
	it receives a list of the inputs and returns a dictionary with all the inputs parsed."""
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

def gather_single_field_input(input_function=input):
	"""Function used to parse individual field data on the v2 of the script,
	it returns a dictionary with all the inputs."""
	field_dict = {}
	field_dict['type'] = input_function("Field type: ").strip()
	field_dict['name'] = input_function("Field name: ").strip()

	column_name = input_function("Column name (Optional): ").strip()
	field_dict['column_name'] = column_name if column_name else camel_to_snake(field_dict['name'])

	relationship = input_function("Relationship (Optional: 1-1, 1-n, n-1, n-n): ").strip()
	field_dict['join_details'] = relationship if relationship else None

	if relationship:
		field_dict['join_column_name'] = input_function("Join column name: ").strip()

	return field_dict

def gather_inputs(input_function=input, version=None, language=None):
	if version is None:
		version = input_function("Which version do you want to use? (v1/v2/v3): ").strip()

	if version == "v3":
		return gather_inputs_gui(language=language)

	group_name = input_function("Enter the group project name (dots-separated): ").strip()
	entity_name = input_function("Enter the entity name (Pascal case): ").strip()

	if language is None:
		language = input_function("Enter the language (US/BR): ").strip()

	table_name = input_function("Enter the table name (snake case): ").strip()
	table_schema = input_function("Enter the table schema: ").strip()
	jdk_version = input_function("Enter the JDK version (11/17): ").strip()

	fields = []

	if version == "v1":
		fields_input = input_function("Enter the fields (semicolon-separated): ").strip()
		fields = parse_fields(fields_input.split(';'))
	elif version == "v2":
		num_fields = int(input_function("Number of fields you want? ").strip())
		for _ in range(num_fields):
			fields.append(gather_single_field_input(input_function))

	# version = v1
	# group_name = "com.example"
	# entity_name = "personHistory"
	# language = "US"
	# table_name = "person_table"
	# table_schema = "public"
	# jdk_version = "11"
	# fields_input = "String-firstName[first_name];Long-age;Date-birthDate;Long-addressName[address];History-history[seq_history]{n-1,seq_history}"

	return {
		'group_name': group_name,
		'entity_name': entity_name,
		'language': language,
		'fields_input': fields,
		'table_name': table_name,
		'table_schema': table_schema,
		'jdk_version': jdk_version,
	}
