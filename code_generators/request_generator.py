from textwrap import dedent

from __init__ import _4_TABS, COMMON_JAVA_TYPES, EMPTY
from language_dictionary import LocalizationDict
from utils import camel_to_pascal

from .base_generator import BaseGenerator


class RequestGenerator(BaseGenerator):

	def __init__(self, group_name: str, entity_name: str, language_dict: LocalizationDict, fields_input: str, table_name: str, table_schema: str, jdk_version: str, complete_package_path: str):
		super().__init__(group_name, entity_name, language_dict, fields_input, table_name, table_schema, jdk_version, complete_package_path)

	def generate(self):
		request_name_pascal = camel_to_pascal(self.entity_name)
		fields_code = []

		for field in self.fields_input:
			f_type = field['type']
			f_name = field['name']

			if f_type not in COMMON_JAVA_TYPES:
				if f_type.startswith(("List<", "Set<", "ArrayList<")):
					f_type = "List<Long>"
					f_name = f"ids{camel_to_pascal(f_name)}"
				elif f_type.startswith("Enum"):
					continue
				else:
					f_type = "Long"
					f_name = f"id{camel_to_pascal(f_name)}"

			fields_code.append(f"{EMPTY if len(fields_code) == 0 else _4_TABS}private {f_type} {f_name};")

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
