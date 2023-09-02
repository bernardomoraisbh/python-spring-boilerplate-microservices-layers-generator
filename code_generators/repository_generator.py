import re
from textwrap import dedent

from utils import camel_to_pascal

from .base_generator import BaseGenerator


class RepositoryGenerator(BaseGenerator):

	def __init__(self, group_name, entity_name, language, fields_input, table_name, table_schema, jdk_version, complete_package_path):
		self.group_name = group_name
		self.entity_name = entity_name
		self.language = language
		self.fields_input = fields_input
		self.table_name = table_name
		self.table_schema = table_schema
		self.jdk_version = jdk_version
		self.complete_package_path = complete_package_path

	def base_repository_generator(self):
		i_base_repository_code = dedent(f"""\
				package {self.group_name}.repository;

				import org.springframework.data.jpa.repository.JpaRepository;
				import org.springframework.data.jpa.repository.Query;
				import java.time.LocalDateTime;
				import org.springframework.data.repository.NoRepositoryBean;
				import org.springframework.data.repository.CrudRepository;

				@NoRepositoryBean
				public interface BaseRepository<T, ID> extends JpaRepository<T, ID>, CrudRepository<T, ID> {{

						@Query(value = "SELECT now() AT TIME ZONE 'UTC'", nativeQuery = true)
						LocalDateTime {'retornarDataBanco' if self.language == 'BR' else 'getDatabaseTime'}();
				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}/repository", "BaseRepository", i_base_repository_code)

	def generate(self):
		self.base_repository_generator()
		repository_code = dedent(f"""\
				package {self.group_name}.repository;

				import {self.group_name}.entity.{self.entity_name};
				import java.util.Optional;

				public interface {self.entity_name}Repository extends BaseRepository<{self.entity_name}, Long> {{

						// ... Default Queries
				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}/repository", f"{self.entity_name}Repository", repository_code)

	def generate_advanced_CRUD_repository(self):
		self.base_repository_generator()

		repository_name_pascal = camel_to_pascal(self.entity_name)
		method_name = 'listarComFiltros' if self.language == 'BR' else 'findByFilters'
		date_field = 'dataFim' if self.language == 'BR' else 'endDate'

		fields_code = f"\t\t\" WHERE 1=1 \" +\n\t\t\t\t\t\t\t\t\" AND {self.entity_name.lower()}.{date_field} IS NULL "

		for field in self.fields_input:
				parts = field.split('-')
				field_type, field_name = parts[0], parts[1].split('[')[0]
				field_name_camel_case = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), field_name)
				fields_code += "\" +"

				if field_type == 'String':
						fields_code += '\n\t\t\t\t\t\t\t\t" AND (:#{\'#searchFilter.' + f'{field_name_camel_case}' + '} IS NULL OR ' + f'{self.entity_name.lower()}.{field_name_camel_case}' + ' LIKE %:#{\'#searchFilter.' + f'{field_name_camel_case}' + '}%) '
				elif field_type.startswith(('List<', 'Set<', 'ArrayList<')):
						fields_code += '\n\t\t\t\t\t\t\t\t" AND (:#{\'#searchFilter.ids' + f'{field_name_camel_case}' + '} IS NULL OR ' + f'{self.entity_name.lower()}.{field_name_camel_case}' + ' IN :#{\'#searchFilter.ids' + f'{field_name_camel_case}' + '}) '
				else:
						fields_code += '\n\t\t\t\t\t\t\t\t" AND (:#{\'#searchFilter.' + f'{field_name_camel_case}' + '} IS NULL OR ' + f'{self.entity_name.lower()}.{field_name_camel_case}' + ' = :#{\'#searchFilter.' + f'{field_name_camel_case}' + '}) '

		query_code = f"""
						@Query("SELECT {self.entity_name.lower()} FROM {repository_name_pascal} {self.entity_name.lower()} " +
						{fields_code}")
						Page<{repository_name_pascal}> {method_name}(@Param("searchFilter") {repository_name_pascal}Request searchFilter, Pageable pageable);
		"""

		repository_code = dedent(f"""\
				package {self.group_name}.repository;

				import java.util.Optional;

				import {self.group_name}.request.{repository_name_pascal}Request;
				import {self.group_name}.entity.{repository_name_pascal};
				import org.springframework.data.domain.Page;
				import org.springframework.data.domain.Pageable;
				import org.springframework.data.jpa.repository.Modifying;
				import org.springframework.data.jpa.repository.Query;
				import org.springframework.data.repository.query.Param;

				public interface {repository_name_pascal}Repository extends BaseRepository<{repository_name_pascal}, Long> {{

						Optional<{repository_name_pascal}> findByIdAnd{camel_to_pascal(date_field)}IsNull(Long id);

						@Modifying
						@Query("UPDATE {repository_name_pascal} e SET e.{date_field} = :#{{#{'retornarDataBanco' if self.language == 'BR' else 'getDatabaseTime'}()}} WHERE e.id = :id")
						void {'excluirLogicamente' if self.language == 'BR' else 'logicalDelete'}(@Param("id") Long id);
						{query_code}
				}}
		""")

		self.write_to_java_file(f"{self.complete_package_path}/repository", f"{repository_name_pascal}Repository", repository_code)
