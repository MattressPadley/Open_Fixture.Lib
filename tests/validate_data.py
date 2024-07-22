import json
import sys
import jsonschema
from jsonschema import validate

REQUIRED_BOOLEAN_FIELDS = [
    "Power.USB_Port",
    "Power.Internal_battery",
    "Control.CRMX",
    "Control.RDM",
    "Control.Ethernet",
    "Control.5_Pin_DMX",
    "Control.3_Pin_DMX",
]

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
    try:
        validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False, str(err)
    return True, ""


def validate_data(data):
    errors = []
    warnings = []

    for field in REQUIRED_BOOLEAN_FIELDS:
        field_value = get_nested_field(data, field)
        if field_value is None:
            errors.append(f"Missing required boolean field: {field}")
        elif not isinstance(field_value, bool):
            errors.append(f"Invalid type for field {field}. Expected boolean.")

    for field in ALL_FIELDS:
        field_value = get_nested_field(data, field)
        if field_value is None:
            warnings.append(f"Missing field: {field}")

    return errors, warnings


def format_markdown(errors, warnings, filename, schema_error=None):
    output = []
    if schema_error:
        output.append(f"### Schema Validation Error in {filename} :x:")
        output.append(f" - **{schema_error}**")
    if errors:
        output.append(f"### Validation Errors in {filename} :x:")
        for error in errors:
            output.append(f" - **{error}**")
    if warnings:
        output.append(f"### Validation Warnings in {filename} :warning:")
        for warning in warnings:
            output.append(f" - *{warning}*")

    if not errors and not warnings and not schema_error:
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

    is_valid, schema_error = validate_json(data, schema)

    errors, warnings = validate_data(data)
    markdown_output = format_markdown(
        errors, warnings, file, schema_error if not is_valid else None
    )

    with open(output_file, "a") as f:
        f.write(markdown_output + "\n\n")

    if errors or schema_error:
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
