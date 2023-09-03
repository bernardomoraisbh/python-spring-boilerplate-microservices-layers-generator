
BR = {
	"Group Project Name": "Nome do Grupo de Projeto",
	"Entity Name": "Nome da Entidade",
	"Language": "Idioma",
	"Table Name": "Nome da Tabela",
	"Table Schema": "Esquema da Tabela",
	"JDK Version": "Versão do JDK",
	"Add Field": "Adicionar Campo",
	"Generate Files": "Gerar Arquivos",
	"Error": "Erro",
	# Add more as needed...
}


class LocalizationDict:
	"""Class used to store the translation of the texts
	used in this program."""

	def __init__(self, language):
		self.language = language
		self.localization_dict = self.get_localization_dict(language)

	def get_localization_dict(self, language):
		if language == "BR":
			return BR
		else:
			return {}  # For "US", no translation needed

	def get_text(self, key):
		"""Function used to get a text from the dictionary based on the
		initially provided language."""
		return self.localization_dict.get(key, key)

