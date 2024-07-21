import json
import sys
import logging

REQUIRED_BOOLEAN_FIELDS = [
    "Power.USB_Power",
    "Power.Battery_Compatible",
    "Control.crmx",
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
    "Power.USB_Power",
    "Power.Battery_Compatible",
    "Optics.Beam_Angle",
    "Optics.Color_Temp",
    "Optics.Source",
    "Optics.LED_Array",
    "Optics.Color",
    "Optics.Pixel_count",
    "Optics.Lens",
    "Control.crmx",
    "Control.RDM",
    "Control.Ethernet_Protocols",
    "Control.Ethernet",
    "Control.5_Pin_DMX",
    "Control.3_Pin_DMX",
    "Physical.mount",
    "Physical.IP_Rating",
]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_data.py <data_file.json>")
        sys.exit(1)

    data_file = sys.argv[1]
    try:
        with open(data_file) as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"Error reading JSON file: {e}")
        sys.exit(1)

    validation_errors, validation_warnings = validate_data(data)

    if validation_errors:
        logging.error("Validation Errors Found:")
        for error in validation_errors:
            logging.error(f" - {error}")
        sys.exit(1)

    if validation_warnings:
        logging.warning("Validation Warnings Found:")
        for warning in validation_warnings:
            logging.warning(f" - {warning}")

    logging.info("All validations passed!")
    sys.exit(0)
