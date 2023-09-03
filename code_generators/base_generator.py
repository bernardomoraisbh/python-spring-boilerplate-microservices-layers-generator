# base_generator.py
import os

from language_dictionary import LocalizationDict


class BaseGenerator:

	def __init__(self, group_name: str, entity_name: str, language_dict: LocalizationDict, fields_input: str, table_name: str, table_schema: str, jdk_version: str, complete_package_path: str):
		self.group_name = group_name
		self.entity_name = entity_name
		self.language_dict = language_dict # Expected to be a LocalizationDict object from the language_dictionary.py file
		self.fields_input = fields_input   # Expected to be a list of dictionaries
		self.table_name = table_name
		self.table_schema = table_schema
		self.jdk_version = jdk_version
		self.complete_package_path = complete_package_path

	def write_to_java_file(self, base_path, file_name, content):
		# common code to write to a file
		os.makedirs(f"{base_path}", exist_ok=True)
		with open(f"{base_path}/{file_name}.java", "w") as f:
			f.write(content)

