from db.utils.json_schemas import SCHEMAS

def create_error_message(errors, json_type):
    error_text = f"Errores en {json_type}: "
    for i, error in enumerate(errors[:3]):
        error_text += f"{i+1}. {error} "
    if len(errors) > 3:
        error_text += f"y {len(errors) - 3} errores más"
    error_text += "\nSe detuvo la subida."
    return error_text.strip()

def validate_json(data, json_type):
    print(f"Validando {json_type}")

    is_valid, message = validate_json_structure(data, json_type)
    if not is_valid:
        return False, message

    items = data[SCHEMAS[json_type]['main_key']]
    return validate_all_items_content(items, json_type)

def validate_json_structure(data, json_type):
    if json_type not in SCHEMAS:
        return False, create_error_message([f"Tipo {json_type} no reconocido"], json_type)

    schema_type = SCHEMAS[json_type]
    main_key = schema_type['main_key']

    if main_key not in data:
        return False, create_error_message([f"Key '{main_key}' no existe"], json_type)
    if not isinstance(data[main_key], list):
        return False, create_error_message([f"'{main_key}' debe ser lista"], json_type)
    items = data[main_key]
    if not items:
        return False, create_error_message([f"Lista {json_type} vacía"], json_type)

    return True, "Estructura válida"

def validate_all_items_content(items, json_type):
    schema_type = SCHEMAS[json_type]
    errors = []

    for i, item in enumerate(items):
        item_errors = validate_item(item, schema_type, i + 1)
        errors.extend(item_errors)
    if errors:
        return False, create_error_message(errors, json_type)

    return True, f"{json_type.title()} validados correctamente"

def validate_item(item, schema, item_number):
    errors = []

    if not isinstance(item, dict):
        errors.append(f"Item {item_number} no es objeto")
        return errors

    for field in schema['required']:
        if field not in item:
            errors.append(f"Item {item_number}: falta '{field}'")

    for field, expected_type in schema['types'].items():
        if field in item and not isinstance(item[field], expected_type):
            type_name = get_type_name(expected_type)
            errors.append(f"Item {item_number}: '{field}' debe ser {type_name}")

    return errors

def get_type_name(expected_type):
    if isinstance(expected_type, tuple):
        return ' o '.join([t.__name__ for t in expected_type])
    return expected_type.__name__
