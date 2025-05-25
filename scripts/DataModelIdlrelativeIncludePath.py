import os
import re

# Define the directory containing the IDL files
idl_directory = "/Users/pschmitt/vscodeEx/UMAA/umaa_data_model/idl/UMAA"

# Define the regex pattern to match #include directives with "UMAA"
include_pattern = re.compile(r'#include\s+"UMAA/(.+)"')

# Function to process a single IDL file
def process_idl_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace "UMAA" with "../../" in #include directives
    updated_content = include_pattern.sub(r'#include "../../\1"', content)

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)

    print(f"Updated: {file_path}")

# Walk through the directory and process each IDL file
for root, _, files in os.walk(idl_directory):
    for file in files:
        if file.endswith(".idl"):
            file_path = os.path.join(root, file)
            process_idl_file(file_path)

print("All IDL files have been updated.")