# base_generator.py
import os

from utils import camel_to_pascal


class BaseGenerator:

	def __init__(self, group_name, entity_name, language, fields_input, table_name, table_schema, jdk_version, complete_package_path):
		self.group_name = group_name
		self.entity_name = entity_name
		self.language = language
		self.fields_input = fields_input # Expected to be a list of dictionaries
		self.table_name = table_name
		self.table_schema = table_schema
		self.jdk_version = jdk_version
		self.complete_package_path = complete_package_path

	def write_to_java_file(self, base_path, file_name, content):
		# common code to write to a file
		os.makedirs(f"{base_path}", exist_ok=True)
		with open(f"{base_path}/{file_name}.java", "w") as f:
			f.write(content)

