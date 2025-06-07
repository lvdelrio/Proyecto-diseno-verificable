def transform_to_float(number_string: str):
    try:
        return float(number_string)
    except ValueError:
        return None