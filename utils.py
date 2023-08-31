
# Helper functions
def camel_to_kebab(camel):
	return ''.join(['-' + i.lower() if i.isupper() else i for i in camel]).lstrip('-')

def camel_to_snake(name):
	return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')

def camel_to_pascal(camel_str):
	return camel_str[0].upper() + camel_str[1:]

def pascal_to_camel(pascal_str):
    return pascal_str[0].lower() + pascal_str[1:]
