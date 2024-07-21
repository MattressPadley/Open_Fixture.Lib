import json
import sys

REQUIRED_BOOLEAN_FIELDS = [
    "Power.USB_Power",
    "Power.Battery_Compatible",
    "Control.crmx",
    "Control.RDM",
    "Control.Ethernet",
    "Control.5_Pin_DMX",
    "Control.3_Pin_DMX",
]

OPTIONAL_STRING_FIELDS = [
    "Name",
    "Manufacturer",
    "Image",
    "Power.AC_voltage",
    "Power.DC_Port",
    "Power.AC_plug",
    "Optics.Beam_Angle",
    "Optics.Color_Temp",
    "Optics.Source",
    "Optics.LED_Array",
    "Optics.Lens",
    "Control.Ethernet_Protocols",
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

    for field in OPTIONAL_STRING_FIELDS:
        field_value = get_nested_field(data, field)
        if field_value is None:
            warnings.append(f"Missing optional string field: {field}")

    return errors, warnings


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_data.py <data_file.json>")
        sys.exit(1)

    data_file = sys.argv[1]
    with open(data_file) as f:
        data = json.load(f)

    validation_errors, validation_warnings = validate_data(data)

    if validation_errors:
        print("Validation Errors Found:")
        for error in validation_errors:
            print(f" - {error}")
        sys.exit(1)

    if validation_warnings:
        print("Validation Warnings Found:")
        for warning in validation_warnings:
            print(f" - {warning}")

    print("All validations passed!")
    sys.exit(0)
