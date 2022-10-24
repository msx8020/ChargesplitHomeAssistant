import logging

import asyncio
import requests
import urllib3
from bs4 import BeautifulSoup

from .const import DOMAIN,CONF_CODE,CHARGEPOINT_SERIAL

_LOGGER = logging.getLogger(__name__)

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "Mozilla/5.0",
}

urllib3.disable_warnings()


class ChargesplitApi:
    def __init__(self, code: str, serial: str) -> None:
        self.host = serial
        self.code = code
        self.serial = serial
        self.base_url = "https://europe-west1-chargesplithome.cloudfunctions.net/secureEndpoint"
        self.headers = HEADERS
        self.headers["Host"] = serial
        self.headers["Origin"] = self.base_url 
     

    def get_data(self) -> dict:
        # create a session with login page
        url = self.base_url
        session = requests.Session()
        data = { "SECRET": self.code, "SERIAL": self.serial}
        response = session.post(url, data=data, verify=False)
        return response.content  

    def test_auth(self) -> dict:
        # create a session with login page
        url = self.base_url
        session = requests.Session()
        data = { "SECRET": self.code, "SERIAL": self.serial}
        response = session.post(url, data=data, verify=False)
        if response.status_code == 200 :
            return response.content
        else:
            raise requests.ConnectionError

        
    def set_pilot_pwr(self,value: str) -> dict:
        _LOGGER.warning("CALLING API")
        url = "https://europe-west1-chargesplithome.cloudfunctions.net/secureEndpoint"
        session = requests.Session()
        data = { "SECRET": self.code, "SERIAL": self.serial, "COMMAND": "PILOTCHANGE","VALUE":value}
        response = session.post(url, data=data, verify=False)
        return response.content  