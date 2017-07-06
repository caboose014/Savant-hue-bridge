# Savant-hue-bridge
A bridge script for Savant to communicate with Philips Hue


NOTE: This profile REQUIRES daVinci software release 8.0 or higher. Any software version below 8.0 will not control this device. 
In order to use the RGB Slider entity you must be running release 5.2.3 or higher - Please note the RGB slider is currently untested and may not work.

To initially sync the hub with our system:
- You must first press the Link button on the Hue Hub, and then send the RegisterDevice command from Savant (this is a custom workflow you need to create).
- Once registration is complete and control is confirmed please search for UserName in "System State"
- Copy the UserName state that is provided for this device from "System State" and paste in TextEdit.app (this is because it copies a plist not the actual state)
- Now copy the string value and paste that into State Variable -> "user_name"; while inspecting the component in Blueprint.
- Re-upload. This should keep Savant and Hue connected after reboot.

Setting IP address and Script Path:
- You are required to update the state variables for this profile to function correctly
- Inspect the component and from the View dropdown box choose 'State Variable'
- Update both the 'bridge_ip' and the 'script_path' variables.
	> 'script_path' is the location where you have copied the companion script (eg: /home/RPM/savant-hue-bridge.py or /Users/RPM/savant-hue-bridge.py)
	> 'bridge_ip' is the IP address of the Philips Hue bridge on your network

Obtaining Scene addresses:
- Upload your configuration to your host and make sure philips hue is connected as stated above
- From System Monitor run the 'EnterSceneSaver' command from the 'Service Events' screen
- Copy the Scene states that are listed for this device from "System State" and paste in TextEdit.app (this is because it copies a plist not the actual state)
- Now copy the string value and paste that into your data table as required
- Re-upload.

To Identify Scenes, the states will be populated with the Scene Code and the Scene name appended. E.G: "Lighting_controller.sceneLights_MEJ8ksJkv9Cp0xE_Relax"
The Scene Code for this is "MEJ8ksJkv9Cp0xE" and the name is "Relax" Put the Scene Code into Address1 of your data Table.
The sceneLights state show you the Bulb IDs that are included in the scene. E.G: "1, 5, 11, 12, 17". This helps to identify what room the scene is for