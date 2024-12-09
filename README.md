# Chargesplit Domus EV WallBox series custom component for Home Assistant


This first integration for Chargesplit Domus Series will let you integrate your wallbox inside Home Assistant as a custom components: 

## Supported Models

- WB132H
- WB332P
- WB332HS
- WB132HS
- WB132PRY
- WB332PRY

## Installation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

Installation is easiest via the [Home Assistant Community Store
(HACS)](https://hacs.xyz/), which is the best place to get third-party
integrations for Home Assistant. Once you have HACS set up, simply click the button below (requires My Homeassistant configured) or
follow the [instructions for adding a custom
repository](https://hacs.xyz/docs/faq/custom_repositories) and then
the integration will be available to install like any other.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=msx8020&repository=ChargesplitHomeAssistant&category=integration)


## Configuration

- Go in SETTINGS -> DEVICE AND SERVICES -> click on ADD INTEGRATION
- Search now for CHARGESPLIT DOMUS
- When prompted for SERIAL and SECRET code insert and click submit
- You will now find in device your wallbox

## Limitations

- Polling time is limited to 60 Seconds 
- You need to wait 1 minute after sending commands to see updates
- A single station is manageable per HA installation 
- Single current transformer models (WB132H / WB332H /WB332P) will show same value in Home and Solar consumption as it's not possible to determine where current transformer has been installed.  WB-132S with 2 current sensors has not this limitation

WHERE DO I FIND MY SECRET CODE? 

To get your secret code please email to support@chargesplit.com indicating your wallbox serial. 
Secret code will then be integrated into app
 


