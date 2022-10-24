# Chargesplit Domus series custom component for Home Assistant

This first integration for Chargesplit Domus Series will let you integrate your wallbox inside Home Assistant as a custom components: 

INSTALLATION INSTRUCTION: 

- COPY Chargesplit folder in your HA custom components folder 
- Restart the server 
- Go in SETTINGS -> DEVICE AND SERVICES -> click on ADD INTEGRATION
- Search now for CHARGESPLIT DOMUS
- When prompted for SERIAL and SECRET code insert and click submit
- You will now find in device your wallbox

LIMITATION:

- Polling time is limited to 60 Seconds 
- You need to wait 1 minute after sending commands to see updates
- A single station is manageable per HA installation 

WHERE DO I FIND MY SECRET CODE? 

To get your secret code please email to support@chargepslit.com indicating your wallbox serial. 
Secret code will then be integrated into app

