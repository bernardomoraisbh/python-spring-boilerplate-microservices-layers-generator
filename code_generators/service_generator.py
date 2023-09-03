import re
from textwrap import dedent

from utils import camel_to_pascal, pascal_to_camel

from .base_generator import BaseGenerator


class ServiceGenerator(BaseGenerator):

	def __init__(self, group_name, entity_name, language, fields_input, table_name, table_schema, jdk_version, complete_package_path):
		super().__init__(group_name, entity_name, language, fields_input, table_name, table_schema, jdk_version, complete_package_path)

	def generate(self):
		service_name_pascal = camel_to_pascal(self.entity_name)
		repo_name = f"{service_name_pascal}Repository"
		repo_name_camel_case = pascal_to_camel(service_name_pascal)
		repo_field_name = f"{repo_name_camel_case}Repository"
		date_field = 'dataFim' if self.language == 'BR' else 'endDate'

		service_code = dedent(f"""\
				package {self.group_name}.services;

				import {self.group_name}.entity.{service_name_pascal};
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
				public class {service_name_pascal}Service {{

						@Autowired
						private {repo_name} {repo_field_name};

						public {service_name_pascal} {'buscarPorId' if self.language == 'BR' else 'findById'}(Long id) {{
								return {repo_field_name}.findByIdAnd{camel_to_pascal(date_field)}
										.orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "{service_name_pascal} {'não encontrado' if self.language == 'BR' else 'not found'}."));
						}}

						public {service_name_pascal}VO {'buscarVoPorId' if self.language == 'BR' else 'findVoById'}(Long id) {{
								return new {service_name_pascal}VO({'buscarPorId' if self.language == 'BR' else 'findById'}(id));
						}}

						public Page<{service_name_pascal}> {'listarComFiltros' if self.language == 'BR' else 'findByFilters'}({service_name_pascal}Request request, Pageable pageable) {{
								return {repo_field_name}.{'listarComFiltros' if self.language == 'BR' else 'findByFilters'}(request, pageable);
						}}

						public Page<{service_name_pascal}VO> {'listarVoFiltrado' if self.language == 'BR' else 'listVoWithFilters'}({service_name_pascal}Request request, Pageable pageable) {{
								Page<{service_name_pascal}> entityList = {'listarComFiltros' if self.language == 'BR' else 'findByFilters'}(request, pageable);
								return new PageImpl<>(entityList.stream().map(x -> new {service_name_pascal}VO(x)).collect(Collectors.toList()), pageable, entityList.getTotalElements());
						}}

						@Transactional
						public void {'excluirLogicamente' if self.language == 'BR' else 'logicalDelete'}(Long id) {{
								{repo_field_name}.{'excluirLogicamente' if self.language == 'BR' else 'logicalDelete'}(id);
						}}
				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}/services", f"{service_name_pascal}Service", service_code)
