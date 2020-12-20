import json


class User:

    def __init__(self, dataFileName):
        with open(dataFileName) as dataFile:
            data = json.load(dataFile)
            user = data["Utente"]
            self.user_data = user["user_data"]
            self.location = user["residenza"]
            self.ad_id = user["ad_id"]
            self.acceleremoter = user["acceleremoter"]
            self.gyroscope = user["gyroscope"]
            self.imei = user["imei"]
            self.mac_address = user["mac-addres"]
            self.contact = user["rubrica"]
            self.serial_number = user["numero_serie"]
            # self.wifi_ssid = user["wifi_ssid"]
            # self.user_id = user["user_id"]
            # self.phone = user["telefono"]
            