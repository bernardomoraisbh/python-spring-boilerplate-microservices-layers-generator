from textwrap import dedent

from .base_generator import BaseGenerator


class VoGenerator(BaseGenerator):

	def __init__(self, group_name, entity_name, language, fields_input, table_name, table_schema, jdk_version, complete_package_path):
		self.group_name = group_name
		self.entity_name = entity_name
		self.language = language
		self.fields_input = fields_input
		self.table_name = table_name
		self.table_schema = table_schema
		self.jdk_version = jdk_version
		self.complete_package_path = complete_package_path

	def generate(self):
		fields_code = ""
		empty_tabs_size = ""
		tabs_size = "\t\t\t\t\t\t"

		for f in self.fields_input:
			field_type = f.split('-')[0]
			attribute_name = f.split('-')[1].split('[')[0]

			if len(fields_code) == 0:
					current_tabs_size = empty_tabs_size
			else:
					current_tabs_size = tabs_size

			field_line = f"{empty_tabs_size if len(fields_code) == 0 else tabs_size}private {field_type} {attribute_name};"
			fields_code += field_line + '\n'

		fields_code = fields_code.rstrip('\n')
		# Generate the constructor that accepts the Entity object
		constructor_code = f"public {self.entity_name}VO({self.entity_name} entity) {{\n"
		constructor_code += "\t\t\t\t\t\t\tif (entity == null) return;\n"
		for field in self.fields_input:
			field_name = field.split('-')[1].split('[')[0]
			constructor_code += f"\t\t\t\t\t\t\tset{field_name[0].upper() + field_name[1:]}(entity.get{field_name[0].upper() + field_name[1:]}());\n"
		constructor_code += "\t\t\t\t\t\t}"

		vo_code = dedent(f"""\
				package {self.group_name}.vo;
				import {self.group_name}.entity.{self.entity_name};
				import lombok.Data;
				import lombok.NoArgsConstructor;
				import com.fasterxml.jackson.annotation.JsonInclude;
				import com.fasterxml.jackson.annotation.JsonInclude.Include;
				import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

				@Data
				@NoArgsConstructor
				@JsonInclude(JsonInclude.Include.NON_ABSENT)
				@JsonIgnoreProperties(ignoreUnknown = true)
				public class {self.entity_name}VO {{

						{fields_code}

						{constructor_code}
				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}/vo", f"{self.entity_name}VO", vo_code)
