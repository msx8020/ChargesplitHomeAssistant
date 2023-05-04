# Chargesplit Domus EV WallBox series custom component for Home Assistant


This first integration for Chargesplit Domus Series will let you integrate your wallbox inside Home Assistant as a custom components: 

SUPPORTED MODELS:

- WB132H
- WB332P
- WB332HS
- WB132HS
- WB132PRY
- WB332PRY

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
- Single current transformer models (WB132H / WB332H /WB332P) will show same value in Home and Solar consumption as it's not possible to determine where current transformer has been installed.  WB-132S with 2 current sensors has not this limitation

WHERE DO I FIND MY SECRET CODE? 

To get your secret code please email to support@chargesplit.com indicating your wallbox serial. 
Secret code will then be integrated into app
 


