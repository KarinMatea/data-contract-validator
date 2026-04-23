from data_contract_validator.validator import load_json_file, validate_users

data = load_json_file("sample_data/users.json")
valid_users, errors = validate_users(data)

print("VALID USERS:")
for user in valid_users:
    print(user.model_dump())

print("\nERRORS:")
for error in errors:
    print(error)
