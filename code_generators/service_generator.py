import re
from textwrap import dedent

from utils import camel_to_pascal, pascal_to_camel

from .base_generator import BaseGenerator


class ServiceGenerator(BaseGenerator):

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
		repo_name = f"I{self.entity_name}Repository"
		repo_name_camel_case = pascal_to_camel(self.entity_name)
		repo_field_name = f"{repo_name_camel_case}Repository"
		date_field = 'dataFim' if self.language == 'BR' else 'endDate'

		service_code = dedent(f"""\
				package {self.group_name}.services;

				import {self.group_name}.entity.{self.entity_name};
				import {self.group_name}.vo.{repo_name};
				import {self.group_name}.repository.{repo_name};
				import org.springframework.beans.factory.annotation.Autowired;
				import org.springframework.data.domain.Page;
				import org.springframework.data.domain.Pageable;
				import org.springframework.http.HttpStatus;
				import org.springframework.data.domain.PageImpl;
				import org.springframework.stereotype.Service;
				import org.springframework.web.server.ResponseStatusException;
				import java.util.Optional;

				@Service
				public class {self.entity_name}Service {{

						@Autowired
						private {repo_name} {repo_field_name};

						public {self.entity_name} {'buscarPorId' if self.language == 'BR' else 'findById'}(Long id) {{
								return {repo_field_name}.findByIdAnd{camel_to_pascal(date_field)}
										.orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "{self.entity_name} {'não encontrado' if self.language == 'BR' else 'not found'}."));
						}}

						public {self.entity_name}VO getVOById(Long id) {{
								return new {self.entity_name}VO({'buscarPorId' if self.language == 'BR' else 'findById'}(id));
						}}

						public Page<{self.entity_name}> {'listarComFiltros' if self.language == 'BR' else 'findByFilters'}({self.entity_name}Request request, Pageable pageable) {{
								return {repo_field_name}.{'listarComFiltros' if self.language == 'BR' else 'findByFilters'}(request, pageable);
						}}

						public Page<{self.entity_name}VO> getVOList({self.entity_name}Request request, Pageable pageable) {{
								Page<{self.entity_name}> entityList = {'listarComFiltros' if self.language == 'BR' else 'findByFilters'}(request, pageable);
								return new PageImpl<>(entityList.stream().map(x -> new {self.entity_name}VO(x)).collect(Collectors.toList()), pageable, entityList.getTotalElements());
						}}

						@Transactional
						public void {'excluirLogicamente' if self.language == 'BR' else 'logicalDelete'}(Long id) {{
								{repo_field_name}.{'excluirLogicamente' if self.language == 'BR' else 'logicalDelete'}(id);
						}}
				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}/services", f"{self.entity_name}Service", service_code)
