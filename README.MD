# Python Script for Java Spring Boilerplate Code Generation

## Description

This utility aims to automate the boilerplate code required to build Spring Boot-based microservices by generating the necessary Java classes for various application layers, such as:

- Entity
- VO (Value Object)
- Request
- Repository
- Service
- Controller

It takes basic entity details and fields as inputs and generates the Java code to speed up the development process.

```sh
# Example usage:
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
Enter JDK version (11/17): 11
```

Should I have created a Gradle task for this with groovy? Yes, probably, but now is too late.

## Features

- Code generation for different layers of Spring Boot application
- Support for custom column names and join columns in entities
- Flexibility to choose the JDK version
- Multilingual support: The generated code can use method names in either Brazilian Portuguese (BR) or American English (US).

## Prerequisites

- Python >=3.11
- JDK 11+

## How To Use

Run the `main.py` script and follow the interactive prompts.

```sh
python main.py
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

## Output

The generated code will be organized in a folder structure following the standard Java package naming conventions.

## Known Issues

Many-to-many relationships currently need to be properly implemented. The POST and PUT for creating and updating an entity are not implemented yet, it would also be cool to auto generate a Converter class for dealing the conversion between Entity, VO and Request or Response.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
