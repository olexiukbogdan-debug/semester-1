print("Hello, world!")
print()


name = "Bogdan"
numeric = 42
integer_number = 7
float_number = 3.5
text = "Python"
is_ready = True
items = ["pen", "notebook", "laptop"]
coordinates = (50.45, 30.52)
student = {"name": name, "course": 1}
unique_numbers = {1, 2, 3, 3}

variables = {
    "name": name,
    "numeric": numeric,
    "integer_number": integer_number,
    "float_number": float_number,
    "text": text,
    "is_ready": is_ready,
    "items": items,
    "coordinates": coordinates,
    "student": student,
    "unique_numbers": unique_numbers,
}

print("Variables, values, and types:")
for variable_name, value in variables.items():
    print(f"{variable_name} = {value!r}; type = {type(value).__name__}")

print()
print("Operators:")
print(f"numeric + integer_number = {numeric + integer_number}")
print(f"numeric - integer_number = {numeric - integer_number}")
print(f"numeric * float_number = {numeric * float_number}")
print(f"numeric / integer_number = {numeric / integer_number}")
print(f"numeric % integer_number = {numeric % integer_number}")
print(f"numeric // integer_number = {numeric // integer_number}")
print(f"integer_number ** 2 = {integer_number ** 2}")
print(f"text + '!' = {text + '!'}")
print(f"text * 2 = {text * 2}")
print(f"items + ['phone'] = {items + ['phone']}")
print(f"items * 2 = {items * 2}")
print(f"coordinates + (1.0,) = {coordinates + (1.0,)}")
print(f"unique_numbers | {{4}} = {unique_numbers | {4}}")
print(f"student['name'] = {student['name']}")
