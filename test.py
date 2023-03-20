file_name = 'context.txt'

print("Attempting to read the file...")

with open(file_name, 'r') as file:
    content = file.read()

print("File read successfully!")

# Check if the content is empty or contains only whitespace characters
if content.strip():
    print("Content of the file:")
    print(content)
else:
    print("The file is empty or contains only whitespace characters.")
