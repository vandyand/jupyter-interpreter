import json

# Read the data from complex_data.json
with open("complex_data.json", "r") as json_file:
    data = json.load(json_file)

# Extract user names
user_names = [user["name"] for user in data["users"]]

# Write user names to user_names.txt
with open("user_names.txt", "w") as output_file:
    for name in user_names:
        output_file.write(name + "
")

