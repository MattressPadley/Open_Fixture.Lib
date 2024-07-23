# Filmset.Lighting Library

This is a library of lighting fixtures for film and television production. The library is intended to be used as the data for the filmset.lighting webpage but I'm making it freely available to anyone who would want to add fixtures or download the data to use themselves.

 The library is organized by fixture type and manufacturer. 

This is a representation of the data schema for fixtures.
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


## Contributing
If you would like to contribute to the library, please follow these steps:  

1. Fork the repository
2. Add your fixture to the appropriate manufacturer folder in the above format
3. Create a pull request


## Tools

### Fixture Scraper

[Fixture Scraper](https://chatgpt.com/g/g-17QCy2rb1-fixture-scraper) is a custom GPT that can help you scrape fixture data from the web. You can use it to extract information from manufacturer websites and other sources and output the correct format.
