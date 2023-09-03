# Python Script for Java Spring Boilerplate Code Generation

## Description

This utility project aims to automate the boilerplate code required to build Spring Boot-based microservices by generating the necessary Java classes for various application layers, such as:

- Entity
- VO (Value Object)
- Request
- Repository
- Service
- Controller

It takes basic entity details and fields as inputs and generates the Java code to speed up the development process.

Should I have created a Gradle task for this with groovy? Yes, probably, but now is too late.

## Features

- Code generation for different layers of Spring Boot application.
- Support for custom column names and join columns in entities.
- Flexibility to choose the JDK version.
- Multilingual support: The generated code can use method names in either Brazilian Portuguese (BR) or American English (US).

## Prerequisites

- Python >=3.11
- JDK 11+ (Probably works with 8+ too)

## How To Use

Run the `main.py` script and follow the interactive prompts.

```sh
python main.py        # For manual data input
```

The script have 3 versions:

v1 - Will prompt you the information needed for generating the files as this example:

```sh
	# version = v1
	# group_name = "com.example"
	# entity_name = "personHistory"
	# language = "US"
	# table_name = "person_table"
	# table_schema = "public"
	# jdk_version = "11"
	# fields_input = "String-firstName[first_name];Long-age;Date-birthDate;Long-addressName[address];History-history[seq_history]{n-1,seq_history}"
```

v2 - It will ask for the same things, but the fields option is a loop, so you can enter every field and property about the field independently:

```sh
# Which version do you want to use? (v1/v2/v3): v2
# Enter the group project name (dots-separated): com.example
# Enter the entity name (Pascal case): PersonHistory
# Enter the language (US/BR): US
# Enter the table name (snake case): person_table
# Enter the table schema: public
# Enter the JDK version (11/17): 11
# Number of fields you want? 5
# Field type: String
# Field name: firstName
# Column name (Optional): first_name
# Relationship (Optional: 1-1, 1-n, n-1, n-n):
# Field type: Long
# Field name: age
# Column name (Optional):
# Relationship (Optional: 1-1, 1-n, n-1, n-n):
# Field type: Date
# Field name: birthDate
# Column name (Optional):
# Relationship (Optional: 1-1, 1-n, n-1, n-n):
# Field type: Long
# Field name: addressName
# Column name (Optional): address
# Relationship (Optional: 1-1, 1-n, n-1, n-n):
# Field type: History
# Field name: history
# Column name (Optional): seq_history
# Relationship (Optional: 1-1, 1-n, n-1, n-n): n-1
# Join column name: seq_history
# Successfully generated the CRUD files.
```

v3 - A GUI interface will open where you can input the same as above and you can also dynamically input or remove new fields.

You can also run the script passing the LANGUAGE (BR/US) AND the VERSION as execution args, as in the examples bellow:

```sh
python main.py US v1  # For US language and version v1
python main.py US v2  # For US language and version v2
python main.py US v3  # For US language and version v3
python main.py BR v1  # For BR language and version v1
python main.py BR v2  # For BR language and version v2
python main.py BR v3  # For BR language and version v3
```


## How to Test

The folder ./tests contains some Unity and Integration tests, the Integration tests are inside test_main.py file and are not properly implemented yet.

```sh
`python -m unittest` # Run inside the tests folder for test everything
`python -m unittest discover -k test_entity_generator` # Run inside the tests folder for testing the entity_generator.py
`python -m unittest discover -k test_vo_generator` # Run inside the tests folder for testing the vo_generator.
`python -m unittest discover -k test_repository_generator` # Run inside the tests folder for testing the repository_generator.py
`python -m unittest discover -k test_service_generator` # Run inside the tests folder for testing the service_generator.py
```

## Input Format

The fields_input expects a specific pattern:

```sh
type-attributeName[column_name]{n-n,joinColumnName}
```

- type: Java type of the field (e.g., String, Long, Date, etc.)
- attributeName: Name of the attribute (e.g., firstName, age, etc.)
- column_name: The column name in the database
- n-n: Cardinality for the relationship (e.g., 1-1 for OneToOne, 1-n for OneToMany, etc.)
- joinColumnName: Name of the join column in the database

Separate each field definition with a semicolon.

## Example

For an entity Person with fields firstName of type String, age of type Long, and birthDate of type Date, the fields_input would be:

```sh
String-firstName[first_name];Long-age;Date-birthDate
```

```sh
# Example usage for the v1 script:
group_name = "com.example"
entity_name = "Person"
fields_input = "String-firstName[first_name];Long-age,Date-birthDate;Long-addressName[address];History-history[seq_history]{n-1,seq_history}"
  # fields should follow this pattern: type-attributeName[column_name]{n-n,joinColumnName} separated by semicolon
table_name = "person_table"
table_schema = "public"
language = "US"
jdk_version = "11"

Enter the group project name (dots-separated): api.system.test
Enter the entity name (pascal case): TestEntity
Enter the language (US/BR): BR
Enter the fields (semicolon-separated): String-label;String-tipo;String-componente[nome_componente];Long-tamanho;Long-limiteCaracteres;Long-cols;Long-lg;String-props
Enter the table name (database table name, using snake case): test_table
Enter the table schema: public
Enter JDK version (11/17): 11 # 11 Uses javax. and 17 uses jakarta.
```


## Output

The generated code will be organized in a folder structure following the standard Java package naming conventions.

## Known Issues

Many-to-many relationships currently need to be properly implemented. The POST and PUT for creating and updating an entity are not implemented yet, it would also be cool to auto generate a Converter class for dealing the conversion between Entity, VO and Request or Response.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
The code was structured focusing on separation of concerns so anyone can easily change something on each generator file without affecting the overall results, this is also valid for input changes and for new languages support, just put your language and translations inside the language_dictionary.py file.
The n-n relationship code generation is not implemented yet, feel free to do it yourself.
