import json


class User:

    def __init__(self, dataFileName):
        with open(dataFileName) as dataFile:
            data = json.load(dataFile)
            user = data["Utente"]
            self.user_data = user["user_data"]
            self.location = user["location"]
            self.ad_id = user["ad_id"]
            self.acceleremoter = user["acceleremoter"]
            self.gyroscope = user["gyroscope"]
            self.imei = user["imei"]
            self.mac_address = user["mac_addres"]
            self.contact = user["contacts"]
            self.serial_number = user["serial_number"]
