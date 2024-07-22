import json
import sys

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


def main(file):
    try:
        with open(file) as f:
            data = json.load(f)
    except Exception as e:
        return f"Error reading JSON file {file}: {e}"

    errors, warnings = validate_data(data)
    output = []

    if errors:
        output.append(f"Validation Errors in {file}:]")
        for error in errors:
            output.append(f" - {error}")
    if warnings:
        output.append(f"Validation Warnings in {file}:")
        for warning in warnings:
            output.append(f" - {warning}")

    if not errors and not warnings:
        output.append(f"All validations passed for {file}!")

    return " ".join(output)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_data.py <data_file.json>")
        sys.exit(1)

    file = sys.argv[1]
    result = main(file)
    print(result)
    if "Validation Errors" in result:
        sys.exit(1)
    else:
        sys.exit(0)
