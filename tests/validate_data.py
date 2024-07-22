import json
import sys
import time
from jsonschema import Draft7Validator


ALL_FIELDS = [
    "Name",
    "Manufacturer",
    "Image",
    "Dimensions.Weight",
    "Dimensions.Height",
    "Dimensions.Width",
    "Dimensions.Depth",
    "Power.AC_voltage",
    "Power.Power_Draw",
    "Power.DC_Port",
    "Power.DC_voltage",
    "Power.AC_plug",
    "Optics.Beam_Angle",
    "Optics.Color_Temp",
    "Optics.Source",
    "Optics.LED_Array",
    "Optics.Color",
    "Optics.Pixel_count",
    "Optics.Lens",
    "Physical.mount",
    "Physical.IP_Rating",
]


def get_nested_field(data, field_path):
    keys = field_path.split(".")
    for key in keys:
        if key in data:
            data = data[key]
        else:
            return None
    return data


def validate_json(data, schema):
    validator = Draft7Validator(schema)
    errors = list(validator.iter_errors(data))
    if errors:
        return False, errors
    return True, []

def format_schema_errors(errors):
    formatted_errors = []
    for error in errors:
        formatted_errors.append(
            f"{'.'.join(map(str, error.path))}: {error.message}"
        )
    return formatted_errors


def validate_data(data):
    warnings = []
    for field in ALL_FIELDS:
        field_value = get_nested_field(data, field)
        if field_value is None:
            warnings.append(f"Missing optional field: {field}")

    return  warnings


def format_markdown(warnings, filename, schema_error=None):
    output = []
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    output.append(f"## Validation Report for:")
    output.append(f"## {filename}")
    output.append(f" {timestamp}")
    if schema_error:
        output.append(f"### :x: Validation Errors {filename} :x:")
        for schema_error in schema_error:
            output.append(f" - {schema_error}")
    if warnings:
        output.append(f"### :warning: Validation Warnings :warning:")
        for warning in warnings:
            output.append(f" - {warning}")

    if not warnings and not schema_error:
        output.append(f"### All validations passed for {filename} :white_check_mark:")

    return "\n".join(output)


def main(file, schema_file, output_file):
    try:
        with open(file) as f:
            data = json.load(f)
    except Exception as e:
        return f"Error reading JSON file {file}: {e}"

    try:
        with open(schema_file) as f:
            schema = json.load(f)
    except Exception as e:
        return f"Error reading JSON schema file {schema_file}: {e}"

    is_valid, schema_errors = validate_json(data, schema)

    warnings = validate_data(data)
    schema_error_messages = (
        format_schema_errors(schema_errors) if not is_valid else None
    )
    markdown_output = format_markdown(
        warnings, file, schema_error_messages if not is_valid else None
    )

    with open(output_file, "a") as f:
        f.write(markdown_output + "\n\n")

    if schema_errors:
        return 1
    else:
        return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python validate_data.py <data_file.json> <schema_file.json> <output_file.md>"
        )
        sys.exit(1)

    file = sys.argv[1]
    schema_file = sys.argv[2]
    output_file = sys.argv[3]
    result = main(file, schema_file, output_file)
    sys.exit(result)
