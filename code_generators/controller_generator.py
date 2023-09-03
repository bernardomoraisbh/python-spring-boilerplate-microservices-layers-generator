import re
from textwrap import dedent

from utils import camel_to_pascal, pascal_to_camel

from .base_generator import BaseGenerator


class ControllerGenerator(BaseGenerator):

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
		entity_name_kebab = ''.join(word.lower() if i == 0 else '-' + word.lower() for i, word in enumerate(re.findall('[A-Z][^A-Z]*', self.entity_name)))
		controller_name = camel_to_pascal(self.entity_name)
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
				public class {controller_name}Controller {{

						private static final Logger logger = LoggerFactory.getLogger({controller_name}Controller.class);

						@Autowired
						private {service_name} {service_field_name};

						@GetMapping(produces = MediaType.APPLICATION_JSON_VALUE)
						public Page<{controller_name}VO> {'listarFiltrado' if self.language == 'BR' else 'listWithFilters'}({controller_name}Request request, @PageableDefault(sort = {{"id"}}, direction = Direction.DESC, size = Integer.MAX_VALUE) Pageable pageable) {{
								logger.info("{controller_name}Controller.{'listarFiltrado' if self.language == 'BR' else 'listWithFilters'}()");
								return {service_field_name}.{'listarVoFiltrado' if self.language == 'BR' else 'listVoWithFilters'}(request, pageable);
						}}

						@GetMapping(path = "/{{id}}", produces = MediaType.APPLICATION_JSON_VALUE)
						public {controller_name}VO {'buscarPorId' if self.language == 'BR' else 'findById'}(@PathVariable Long id) {{
								logger.info("{controller_name}Controller.{'buscarPorId' if self.language == 'BR' else 'findById'}({{}})", id);
								return {service_field_name}.{'buscarVoPorId' if self.language == 'BR' else 'findVoById'}(id);
						}}

						@PostMapping(path = "/{{id}}")
						public void {'salvar' if self.language == 'BR' else 'saveEntity'}(@PathVariable Long id) {{
								logger.info("{controller_name}Controller.{'salvar' if self.language == 'BR' else 'saveEntity'}({{}})", id);
								// TODO - TODO
						}}

						@PutMapping(path = "/{{id}}")
						public void {'editar' if self.language == 'BR' else 'updateEntity'}(@PathVariable Long id) {{
								logger.info("{controller_name}Controller.{'editar' if self.language == 'BR' else 'updateEntity'}({{}})", id);
								// TODO - TODO
						}}

						@DeleteMapping(path = "/{{id}}")
						@ResponseStatus(HttpStatus.ACCEPTED)
						public void {'excluir' if self.language == 'BR' else 'deleteEntity'}(@PathVariable Long id) {{
								logger.info("{controller_name}Controller.{'excluir' if self.language == 'BR' else 'deleteEntity'}({{}})", id);
								{service_field_name}.{'excluirLogicamente' if self.language == 'BR' else 'logicalDelete'}(id);
						}}
				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}/controller", f"{controller_name}Controller", controller_code)
