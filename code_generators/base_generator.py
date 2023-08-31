# base_generator.py
import os


class BaseGenerator:

	def write_to_java_file(self, base_path, file_name, content):
		# common code to write to a file
		os.makedirs(f"{base_path}", exist_ok=True)
		with open(f"{base_path}/{file_name}.java", "w") as f:
			f.write(content)

