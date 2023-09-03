import argparse

from code_generators.controller_generator import ControllerGenerator
from code_generators.entity_generator import EntityGenerator
from code_generators.repository_generator import RepositoryGenerator
from code_generators.request_generator import RequestGenerator
from code_generators.service_generator import ServiceGenerator
from code_generators.vo_generator import VoGenerator
from directory_handler import create_directories
from input_handler import gather_inputs, parse_arguments

# Example usage:
# group_name = "com.example"
# entity_name = "Person"
# fields_input = "String-firstName[first_name];Long-age;Date-birthDate;Long-addressName[address];History-history[seq_history]{n-1,seq_history}"
#  fields should follow this pattern type-attributeName[column_name]{n-n,joinColumnName} separated by semicolon
# table_name = "person_table"
# table_schema = "public"
# language = "US"
# jdk_version = "11"

# Many to Many needs to be fixed

def main():
	language, version = parse_arguments()
	user_inputs = gather_inputs(version=version, language=language)
	if user_inputs is None:
		print("Operation cancelled by the user.")
		return
	complete_package_path = create_directories(user_inputs['group_name'].replace('.', '-'), user_inputs['group_name'])

	# Create a list of generator classes to iterate through
	generators = [
		EntityGenerator,
		VoGenerator,
		RequestGenerator,
		RepositoryGenerator,
		ServiceGenerator,
		ControllerGenerator
	]

	# Loop through each generator class and create an instance, then generate the code
	for generator_class in generators:
		generator_instance = generator_class(
				group_name=user_inputs['group_name'],
				entity_name=user_inputs['entity_name'],
				language_dict=user_inputs['language_dict'],
				fields_input=user_inputs['fields_input'],
				table_name=user_inputs['table_name'],
				table_schema=user_inputs['table_schema'],
				jdk_version=user_inputs['jdk_version'],
				complete_package_path=complete_package_path,
		)
		if isinstance(generator_instance, RepositoryGenerator):
			generator_instance.generate_advanced_CRUD_repository()
		else:
			generator_instance.generate()
	print("CRUD gerado com sucesso." if user_inputs['language'] == "BR" else "Successfully generated the CRUD files.")

if __name__ == "__main__":
	main()
