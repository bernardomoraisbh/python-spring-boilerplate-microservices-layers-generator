import re
import sys
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk

data = {}
fields = []
font=("Arial", 20)

def gather_inputs_gui():

	def _on_mousewheel(event):
		canvas.yview_scroll(-1*(event.delta//120), "units")

	def add_field():
		field_frame = ttk.Frame(fields_frame)
		field_frame.grid(row=len(fields), column=0, sticky="w")

		ttk.Label(field_frame, text=f"Field {len(fields) + 1}", style="Large.TLabel").grid(row=0, column=0, columnspan=4)

		ttk.Label(field_frame, text="Type: ", style="Large.TLabel").grid(row=1, column=0)
		type_entry = ttk.Entry(field_frame, font=font)
		type_entry.grid(row=1, column=1)

		ttk.Label(field_frame, text="Name: ", style="Large.TLabel").grid(row=1, column=2)
		name_entry = ttk.Entry(field_frame, font=font)
		name_entry.grid(row=1, column=3)

		ttk.Label(field_frame, text="Column Name: ", style="Large.TLabel").grid(row=2, column=0)
		column_name_entry = ttk.Entry(field_frame, font=font)
		column_name_entry.grid(row=2, column=1)

		ttk.Label(field_frame, text="Join Details: ", style="Large.TLabel").grid(row=2, column=2)
		join_details_entry = ttk.Entry(field_frame, font=font)
		join_details_entry.grid(row=2, column=3)

		ttk.Label(field_frame, text="Join Column Name: ", style="Large.TLabel").grid(row=3, column=0)
		join_column_name_entry = ttk.Entry(field_frame, font=font)
		join_column_name_entry.grid(row=3, column=1)

		# Add more field entries as needed

		remove_button = ttk.Button(field_frame, text="Remove", style="Large.TButton", command=lambda: remove_field(field_frame))
		remove_button.grid(row=1, column=4)

		fields.append((field_frame, type_entry, name_entry))
		fields_frame.update_idletasks()
		canvas.config(scrollregion=canvas.bbox("all"))

	def remove_field(frame):
		frame.grid_forget()
		for field_tuple in fields:
			field_frame, _, _ = field_tuple
			if field_frame == frame:
				fields.remove(field_tuple)
				break

	def validate_fields():
		if not group_name_entry.get():
			messagebox.showerror("Error", "Field group name cannot be empty!")
			return False

		if not entity_name_entry.get():
			messagebox.showerror("Error", "Field entity name cannot be empty!")
			return False

		if not language_entry.get():
			messagebox.showerror("Error", "Field language cannot be empty!")
			return False
		elif language_entry.get() not in ['US', 'BR']:
			messagebox.showerror("Error", "Field language must be either 'US' or 'BR'!")
			return False

		if not table_name_entry.get():
			messagebox.showerror("Error", "Field table name cannot be empty!")
			return False

		if not jdk_version_entry.get():
			messagebox.showerror("Error", "Field jdk version cannot be empty!")
			return False
		elif jdk_version_entry.get() not in ['11', '17']:
			messagebox.showerror("Error", "Field jdk version must be either '11' or '17'!")
			return False

		for field_frame, type_entry, name_entry, column_name_entry, join_details_entry, join_column_name_entry in fields:
			type_value = type_entry.get().strip()
			name_value = name_entry.get().strip()
			column_name = column_name_entry.get(),
			join_details =  join_details_entry.get(),
			join_column_name = join_column_name_entry.get()

			if not type_value or not name_value:
				messagebox.showerror("Error", "Fields type value and name value cannot be empty!")
				return False
			elif not join_details and join_column_name:
				messagebox.showerror("Error", "When join column is present, join details name must be present!")
				return False
			elif join_details and not join_column_name:
				messagebox.showerror("Error", "When join details is present, join column name must be present!")
				return False

		return True

	def submit():
		if validate_fields():
			data.update({
				'group_name': group_name_entry.get(),
				'entity_name': entity_name_entry.get(),
				'language': language_entry.get(),
				'table_name': table_name_entry.get(),
				'table_schema': table_schema_entry.get(),
				'jdk_version': jdk_version_entry.get(),
			})

			data['fields_input'] = []
			for type_entry, name_entry, column_name_entry, join_details_entry, join_column_name_entry in fields:
				field_dict = {
					'type': type_entry.get(),
					'name': name_entry.get(),
					'column_name': column_name_entry.get(),
					'join_details': join_details_entry.get(),
					'join_column_name': join_column_name_entry.get()
					# Add other attributes as needed
				}
				data['fields_input'].append(field_dict)
			root.quit()

	root = tk.Tk()
	root.geometry("1300x800")

	# Configure style for Button, Label and Entry
	style = ttk.Style()
	style.configure("Large.TButton", font=font)
	style.configure("Large.TLabel", font=font)
	style.configure("Large.TEntry", font=font)

	root.title("Input Fields")

	group_name_label = ttk.Label(root, style="Large.TLabel", text="Group Project Name:")
	group_name_entry = ttk.Entry(root, font=font)
	group_name_label.grid(row=0, column=0)
	group_name_entry.grid(row=0, column=1)

	entity_name_label = ttk.Label(root, style="Large.TLabel", text="Entity Name:")
	entity_name_entry = ttk.Entry(root, font=font)
	entity_name_label.grid(row=1, column=0)
	entity_name_entry.grid(row=1, column=1)

	language_label = ttk.Label(root, style="Large.TLabel", text="Language:")
	language_entry = ttk.Entry(root, font=font)
	language_label.grid(row=2, column=0)
	language_entry.grid(row=2, column=1)

	table_name_label = ttk.Label(root, style="Large.TLabel", text="Table Name:")
	table_name_entry = ttk.Entry(root, font=font)
	table_name_label.grid(row=3, column=0)
	table_name_entry.grid(row=3, column=1)

	table_schema_label = ttk.Label(root, style="Large.TLabel", text="Table Schema:")
	table_schema_entry = ttk.Entry(root, font=font)
	table_schema_label.grid(row=4, column=0)
	table_schema_entry.grid(row=4, column=1)

	jdk_version_label = ttk.Label(root, style="Large.TLabel", text="JDK Version:")
	jdk_version_entry = ttk.Entry(root, )
	jdk_version_label.grid(row=5, column=0)
	jdk_version_entry.grid(row=5, column=1)

	fields_frame = ttk.LabelFrame(root, text="Fields")
	fields_frame.grid(row=6, columnspan=2, sticky="w")

	add_field_button = ttk.Button(root, text="Add Field", style="Large.TButton", command=add_field)
	add_field_button.grid(row=7, column=0, sticky="w")

	submit_button = ttk.Button(root, text="Submit", style="Large.TButton", command=submit)
	submit_button.grid(row=7, column=1, sticky="e")

	# Create the outer frame
	outer_frame = ttk.Frame(root)
	outer_frame.grid(row=6, columnspan=2, sticky="w")

	# Create a canvas inside the outer frame
	canvas = tk.Canvas(outer_frame, width=1200, height=500)
	scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)

	fields_frame = ttk.Frame(canvas)

	canvas.pack(side="left", fill="both", expand=True)
	scrollbar.pack(side="right", fill="y")

	canvas.create_window((0, 0), window=fields_frame, anchor="nw")
	canvas.configure(yscrollcommand=scrollbar.set)
	canvas.bind_all("<MouseWheel>", _on_mousewheel)

	add_field_button = ttk.Button(root, text="Add Field", style="Large.TButton", command=add_field)
	add_field_button.grid(row=7, column=0, sticky="w")

	submit_button = ttk.Button(root, text="Submit", style="Large.TButton", command=submit)
	submit_button.grid(row=7, column=1, sticky="e")

	root.mainloop()

	if 'group_name' not in data:
		print("Application closed by the user.")
		sys.exit(1)

	return data
