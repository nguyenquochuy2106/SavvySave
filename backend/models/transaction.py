# Read authentication route file to check its content
auth_py_path = os.path.join(extract_folder, "backend", "routes", "auth.py")

with open(auth_py_path, "r", encoding="utf-8") as file:
    auth_py_content = file.read()

# Display the first 50 lines for review
auth_py_content[:2000]
