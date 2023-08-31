from utils import camel_to_kebab


def gather_inputs():
	# Gather user inputs
	group_name = input("Enter the group project name (dots-separated): ")
	entity_name = input("Enter the entity name (pascal case): ")
	language = input("Enter the language (US/BR): ")
	fields_input = input("Enter the fields (semicolon-separated): ")
	table_name = input("Enter the table name (database table name, using snake case): ")
	table_schema = input("Enter the table schema: ")
	jdk_version = input("Enter JDK version (11/17): ")
	fields = fields_input.split(';')

	# group_name = "api.sistema.registro"
	# entity_name = "CamposAverbacoes"
	# language = "BR"
	# fields_input = "String-label;String-tipo;String-componente[nome_componente];Long-tamanho;Long-limiteCaracteres;Long-cols;Long-lg;String-props"
	# table_name = "campos_averbacoes"
	# table_schema = "registro"
	# jdk_version = "11"
	# fields = fields_input.split(';')


	return {
			'group_name': group_name.strip(),
			'entity_name': entity_name,
			'language': language,
			'fields_input': [attr.strip() for attr in fields],
			'table_name': table_name,
			'table_schema': table_schema,
			'jdk_version': jdk_version,
	}
