# entity_generator.py
import re
from textwrap import dedent

from utils import camel_to_pascal, camel_to_snake

from .base_generator import BaseGenerator


class EntityGenerator(BaseGenerator):

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
		annotations_package = "javax.persistence" if self.jdk_version == "11" else "jakarta.persistence"
		field_code = ""
		field_code_lines = []
		empty_tabs_size = ""
		tabs_size = "\t\t\t\t"
		entity_name_pascal = camel_to_pascal(self.entity_name)

		for field in self.fields_input:
				parts = field.split("-")
				field_type = parts[0]
				attr_and_column = parts[1]

				attribute_parts = attr_and_column.split("[")
				attribute_name = attribute_parts[0]

				column_name = attribute_parts[1][:-1] if '[' in attr_and_column and ']' in attr_and_column else camel_to_snake(attribute_name)
				join_details = None

				if "{" in attr_and_column and "}" in attr_and_column:
						join_details = re.search(r"\{(.+?)\}", attr_and_column).group(1).split(",")

				if "Date" in attribute_name or "Data" in attribute_name or "date" in attribute_name or "data" in attribute_name:
						field_type = "LocalDateTime"
						temporal_annotation = f'@Temporal(TemporalType.TIMESTAMP)'
				else:
						temporal_annotation = ""

				join_annotation = ""

				if join_details:
						join_type = join_details[0]
						join_column_name = join_details[1] if len(join_details) > 1 else column_name

						if join_type == "1-1":
								join_annotation = f'@OneToOne(fetch = FetchType.LAZY)\n				@JoinColumn(name = "{join_column_name}")'
						elif join_type == "1-n":
								join_annotation = f'@OneToMany(mappedBy = "{attribute_name}", fetch = FetchType.LAZY, cascade = {{CascadeType.PERSIST, CascadeType.MERGE, CascadeType.REFRESH}}, orphanRemoval = true)'
						elif join_type == "n-1":
								join_annotation = f'@ManyToOne(fetch = FetchType.LAZY)\n				@JoinColumn(name = "{join_column_name}")'
						elif join_type == "n-n":
								join_annotation = f'@ManyToMany(fetch = FetchType.LAZY)\n				@JoinColumn(name = "{join_column_name}")'

				if join_annotation:
						field_code_lines.append(f"{empty_tabs_size if len(field_code_lines) == 0 else tabs_size}{join_annotation}")
				field_code_lines.append(f"{empty_tabs_size if len(field_code_lines) == 0 else tabs_size}@Column(name = \"{column_name}\")")
				if temporal_annotation:
						field_code_lines.append(f"{empty_tabs_size if len(field_code_lines) == 0 else tabs_size}{temporal_annotation}")
				field_code_lines.append(f"{empty_tabs_size if len(field_code_lines) == 0 else tabs_size}private {field_type} {attribute_name};")

				field_code = "\n".join(field_code_lines)

		field_code = field_code.replace(";\n", ";\n\n\t\t").replace(")\n", ")\n\t\t")
		version_field = "versao" if self.language == "BR" else "version"

		entity_code = dedent(f"""\
				package {self.group_name}.entity;

				import lombok.Data;
				import {annotations_package}.*;
				import java.time.LocalDateTime;
				import javax.persistence.Temporal;
				import javax.persistence.TemporalType;
				import javax.persistence.CascadeType;
				import javax.persistence.FetchType;

				@Data
				@Table(name = "{self.table_name}", schema = "{self.table_schema}")
				@SequenceGenerator(name = "seq_{self.table_name}", sequenceName = "seq_{self.table_name}", allocationSize = 1)
				public class {entity_name_pascal} {{

						@Id
						@GeneratedValue(strategy = GenerationType.AUTO, generator = "seq_id_{self.table_name}")
						@Column(name = "seq_id_{self.table_name}")
						private Long id;

						{field_code}

						@Version
						private Integer {version_field};
				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}/entity", entity_name_pascal, entity_code)
