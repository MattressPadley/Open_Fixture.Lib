# Open_Fixture.Lib

```json
{
  "Name": "Fixture Name",
  "Manufacturer": "Manufacturer Name",
  "Image": "Image URL", //must be an image format
  "Manual": "Link to Manual",
  "Dimensions": {
    "Weight": Number, // Weight in pounds
    "Height": Number, // Height in inches
    "Width": Number, // Width in inches
    "Depth": Number // Depth in inches
  },
  "Power": {
    "AC_voltage": "AC voltage range",
    "Power_Draw": Number, // Power draw in watts
    "DC_Port": "DC port type", //type and number of pins if applicable
    "DC_voltage": "DC input voltage range", // Specify the range if available, otherwise the nominal voltage
    "AC_plug": "AC plug type", // Edison, 100a 110v Bates, 60a 110v Bates, etc
    "USB_Port": true/false,
   "Internal_battery":true/false
  },
  "Optics": {
    "Beam_Angle": "Beam angle in degrees with degree symbol",
    "Color_Temp": "Color temperature range",
    "Source": "Light source type", // e.g., "LED", "HMI", "Tungsten"
    "LED_Array": "LED array type", // e.g., "RGBA", "RGBACL"
    "Color": true/false,
    "Pixel_count": Number, // Number of pixels
    "Lens": "Lens type" // Example: "10 inch Fresnel"
  },
  "Control": {
    "CRMX": true/false,
    "RDM": true/false,
    "Ethernet": true/false,
    "5_Pin_DMX": true/false,
    "3_Pin_DMX": true/false
  },
  "Physical": {
    "mount": "Mount type", // Junior Pin, Baby Pin
    "IP_Rating": "IP rating"
  }
}
```