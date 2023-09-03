import os

from __init__ import SRC_MAIN_JAVA


# complete_package_path
def create_directories(parent_folder_name, group_name):
	os.makedirs(f"{parent_folder_name}/{SRC_MAIN_JAVA}/{group_name.replace('.', '/')}", exist_ok=True)
	return f"{parent_folder_name}/src/main/java/{group_name.replace('.', '/')}"
