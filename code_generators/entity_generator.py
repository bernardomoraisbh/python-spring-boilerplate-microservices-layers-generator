# entity_generator.py
import re
from textwrap import dedent

from __init__ import _4_TABS, EMPTY
from language_dictionary import LocalizationDict
from utils import camel_to_pascal, camel_to_snake

from .base_generator import BaseGenerator


class EntityGenerator(BaseGenerator):

	def __init__(self, group_name: str, entity_name: str, language_dict: LocalizationDict, fields_input: str, table_name: str, table_schema: str, jdk_version: str, complete_package_path: str):
		super().__init__(group_name, entity_name, language_dict, fields_input, table_name, table_schema, jdk_version, complete_package_path)

	def temporal_annotation(self, attribute_name):
		temporal_annotation = ""
		if "Date" in attribute_name or "Data" in attribute_name or "date" in attribute_name or "data" in attribute_name:
			temporal_annotation = '@Temporal(TemporalType.TIMESTAMP)'
		return temporal_annotation

	def parse_join(self, field_dict, field_code_lines, attribute_name):
		join_details = field_dict['join_details']
		join_annotation = ""

		if join_details:
			if ',' not in join_details:
				print(f"Warning: Invalid join_details format for {field_dict['name']}. Expected 'type,column', got '{join_details}'")
				return
			join_type, join_column_name = join_details.split(",")

			if join_type == "1-1":
					join_annotation = f'@OneToOne(fetch = FetchType.LAZY)\n				@JoinColumn(name = "{join_column_name}")'
			elif join_type == "1-n":
					join_annotation = f'@OneToMany(mappedBy = "{attribute_name}", fetch = FetchType.LAZY, cascade = {{CascadeType.PERSIST, CascadeType.MERGE, CascadeType.REFRESH}}, orphanRemoval = true)'
			elif join_type == "n-1":
					join_annotation = f'@ManyToOne(fetch = FetchType.LAZY)\n				@JoinColumn(name = "{join_column_name}")'
			elif join_type == "n-n":
					join_annotation = f'@ManyToMany(fetch = FetchType.LAZY)\n				@JoinColumn(name = "{join_column_name}")'

		if join_annotation:
			field_code_lines.append(f"{EMPTY if len(field_code_lines) == 0 else _4_TABS}{join_annotation}")

	def generate_field_code(self):
		field_code_lines = []
		for field_dict in self.fields_input:
			field_type = field_dict['type']
			attribute_name = field_dict['name']
			column_name = field_dict['column_name'] if field_dict['column_name'] else camel_to_snake(attribute_name)

			temporal_annotation = self.temporal_annotation(attribute_name)

			self.parse_join(field_dict, field_code_lines, attribute_name)
			field_code_lines.append(f"{EMPTY if len(field_code_lines) == 0 else _4_TABS}@Column(name = \"{column_name}\")")

			if temporal_annotation:
				field_code_lines.append(f"{EMPTY if len(field_code_lines) == 0 else _4_TABS}{temporal_annotation}")

			field_code_lines.append(f"{EMPTY if len(field_code_lines) == 0 else _4_TABS}private {field_type} {attribute_name};")

		field_code = "\n".join(field_code_lines).replace(";\n", ";\n\n\t\t").replace(")\n", ")\n\t\t")
		return field_code

	def generate(self):
		annotations_package = "javax.persistence" if self.jdk_version == "11" else "jakarta.persistence"
		entity_name_pascal = camel_to_pascal(self.entity_name)

		version_field = self.language_dict.get_text("version")

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
				@SequenceGenerator(name = "seq_id_{self.table_name}", sequenceName = "seq_id_{self.table_name}", allocationSize = 1)
				public class {entity_name_pascal} {{

						@Id
						@GeneratedValue(strategy = GenerationType.AUTO, generator = "seq_id_{self.table_name}")
						@Column(name = "seq_{self.table_name}")
						private Long id;

						{self.generate_field_code()}

						@Version
						private Integer {version_field};
				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}/entity", entity_name_pascal, entity_code)
