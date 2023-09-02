from textwrap import dedent

from __init__ import COMMON_JAVA_TYPES
from utils import camel_to_pascal

from .base_generator import BaseGenerator


class RequestGenerator(BaseGenerator):

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
		request_name_pascal = camel_to_pascal(self.entity_name)
		fields_code = []
		empty_tabs_size = ""
		tabs_size = "\t\t\t\t"
		for f in self.fields_input:
			f_type, f_name = f.split('-')[0], f.split('-')[1].split('[')[0]

			if f_type not in COMMON_JAVA_TYPES:
					if f_type.startswith(("List<", "Set<", "ArrayList<")):
							f_type = "List<Long>"
							f_name = f"ids{camel_to_pascal(f_name)}"
					else:
							f_type = "Long"
							f_name = f"id{camel_to_pascal(f_name)}"

			fields_code.append(f"{empty_tabs_size if len(fields_code) == 0 else tabs_size}private {f_type} {f_name};")

		fields_code = '\n\t\t'.join(fields_code)

		request_code = dedent(f"""\
				package {self.group_name}.request;

				import lombok.Data;
				import lombok.NoArgsConstructor;
				import com.fasterxml.jackson.annotation.JsonInclude;
				import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

				@Data
				@NoArgsConstructor
				@JsonInclude(JsonInclude.Include.NON_ABSENT)
				@JsonIgnoreProperties(ignoreUnknown = true)
				public class {request_name_pascal}Request {{
						{fields_code}
				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}/request", f"{request_name_pascal}Request", request_code)
