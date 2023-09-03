import re
from textwrap import dedent

from language_dictionary import LocalizationDict
from utils import camel_to_pascal, pascal_to_camel

from .base_generator import BaseGenerator


class ControllerGenerator(BaseGenerator):

	def __init__(self, group_name: str, entity_name: str, language_dict: LocalizationDict, fields_input: str, table_name: str, table_schema: str, jdk_version: str, complete_package_path: str):
		super().__init__(group_name, entity_name, language_dict, fields_input, table_name, table_schema, jdk_version, complete_package_path)

	def generate(self):
		entity_name_kebab = ''.join(word.lower() if i == 0 else '-' + word.lower() for i, word in enumerate(re.findall('[A-Z][^A-Z]*', self.entity_name)))
		controller_name = f"{camel_to_pascal(self.entity_name)}Controller"
		service_name = f"{self.entity_name}Service"
		service_name_camel_case = pascal_to_camel(self.entity_name)
		service_field_name = f"{service_name_camel_case}Service"

		controller_code = dedent(f"""\
				package {self.group_name}.controller;

				import {self.group_name}.services.{service_name};
				import {self.group_name}.vo.{self.entity_name}VO;
				import {self.group_name}.request.{self.entity_name}Request;
				import org.slf4j.Logger;
				import org.slf4j.LoggerFactory;
				import org.springframework.beans.factory.annotation.Autowired;
				import org.springframework.data.domain.Page;
				import org.springframework.data.domain.Pageable;
				import org.springframework.data.web.PageableDefault;
				import org.springframework.data.domain.Sort.Direction;
				import org.springframework.data.web.PageableDefault;
				import org.springframework.http.HttpStatus;
				import org.springframework.http.ResponseEntity;
				import org.springframework.http.MediaType;
				import org.springframework.web.bind.annotation.*;

				@RestController
				@RequestMapping("/{'/'.join(entity_name_kebab.split('-'))}")
				@CrossOrigin("*")
				public class {controller_name} {{

						private static final Logger logger = LoggerFactory.getLogger({controller_name}.class);

						@Autowired
						private {service_name} {service_field_name};

						@GetMapping(produces = MediaType.APPLICATION_JSON_VALUE)
						public Page<{controller_name}VO> {self.language_dict.get_text('listWithFilters')}({controller_name}Request request, @PageableDefault(sort = {{"id"}}, direction = Direction.DESC, size = Integer.MAX_VALUE) Pageable pageable) {{
								logger.info("{controller_name}.{self.language_dict.get_text('listWithFilters')}()");
								return {service_field_name}.{self.language_dict.get_text('listVoWithFilters')}(request, pageable);
						}}

						@GetMapping(path = "/{{id}}", produces = MediaType.APPLICATION_JSON_VALUE)
						public {controller_name}VO {self.language_dict.get_text('findById')}(@PathVariable Long id) {{
								logger.info("{controller_name}.{self.language_dict.get_text('findById')}({{}})", id);
								return {service_field_name}.{self.language_dict.get_text('findVoById')}(id);
						}}

						@PostMapping(path = "/{{id}}")
						public void {self.language_dict.get_text('saveEntity')}(@PathVariable Long id) {{
								logger.info("{controller_name}.{self.language_dict.get_text('saveEntity')}({{}})", id);
								// TODO - TODO
						}}

						@PutMapping(path = "/{{id}}")
						public void {self.language_dict.get_text('updateEntity')}(@PathVariable Long id) {{
								logger.info("{controller_name}.{self.language_dict.get_text('updateEntity')}({{}})", id);
								// TODO - TODO
						}}

						@DeleteMapping(path = "/{{id}}")
						@ResponseStatus(HttpStatus.ACCEPTED)
						public void {self.language_dict.get_text('deleteEntity')}(@PathVariable Long id) {{
								logger.info("{controller_name}.{self.language_dict.get_text('deleteEntity')}({{}})", id);
								{service_field_name}.{self.language_dict.get_text('logicalDelete')}(id);
						}}
				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}/controller", f"{controller_name}", controller_code)
