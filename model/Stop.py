from datetime import datetime, timezone
from pytz import timezone


class Stop:
    type = ''
    dest = ''
    plannedTime = ''
    estTime = ''

    def __init__(self, stop) -> None:
        self.plannedTime = stop['departureTimePlanned']
        if 'realtimeStatus' in stop and 'MONITORED' in stop['realtimeStatus']:
            self.estTime = stop['departureTimeEstimated']
        else:
            self.estTime = None
        self.time = self.getTime()
        self.dest = stop['transportation']['destination']['name']
        self.type = stop['transportation']['disassembledName']

    def __str__(self):
        return f'{self.type[:3]:<3} {self.dest[:22]:<22} {self.time}'

    def getTime(self):
        planned = datetime.strptime(self.plannedTime, '%Y-%m-%dT%H:%M:%S%z').astimezone(timezone('Europe/Berlin'))
        string = planned.strftime("%H:%M")
        if self.estTime:
            est = datetime.strptime(self.estTime, '%Y-%m-%dT%H:%M:%S%z').astimezone(timezone('Europe/Berlin'))
            diff = (est - planned).total_seconds() / 60.0
            string += f' +{int(diff)}'
        return string


if __name__ == '__main__':
    stop_data = {
        "realtimeStatus": [
            "MONITORED"
        ],
        "isRealtimeControlled": True,
        "location": {
            "id": "de:05911:5194:98:7",
            "isGlobalId": True,
            "name": "Bochum Hbf",
            "disassembledName": "7",
            "type": "platform",
            "pointType": "TRACK",
            "coord": [
                5293616.0,
                804145.0
            ],
            "properties": {
                "occupancy": "MANY_SEATS",
                "stopId": "20005194",
                "area": "98",
                "platform": "7",
                "platformName": "7"
            },
            "parent": {
                "id": "de:05911:5194",
                "isGlobalId": True,
                "name": "Bochum Hbf",
                "disassembledName": "Hbf",
                "type": "stop",
                "parent": {
                    "id": "placeID:5911000:3",
                    "name": "Bochum",
                    "type": "locality"
                },
                "properties": {
                    "stopId": "20005194"
                }
            }
        },
        "departureTimePlanned": "2022-02-10T13:33:00Z",
        "departureTimeEstimated": "2022-02-10T13:36:00Z",
        "transportation": {
            "id": "ddb:92E01: :R:j22",
            "name": "S-Bahn S1",
            "disassembledName": "S1",
            "number": "S1",
            "product": {
                "id": 3,
                "class": 1,
                "name": "S-Bahn",
                "iconId": 2
            },
            "operator": {
                "code": "DBNW",
                "id": "8003",
                "name": "DB Regio AG NRW"
            },
            "destination": {
                "id": "20009289",
                "name": "Essen Hauptbahnhof",
                "type": "stop"
            },
            "properties": {
                "trainName": "S-Bahn",
                "trainType": "S",
                "trainNumber": "31124",
                "tripCode": 633,
                "lineDisplay": "LINE"
            },
            "origin": {
                "id": "20000131",
                "name": "Dortmund Hbf",
                "type": "stop"
            }
        },
        "hints": [
            {
                "content": "Linie S1: Maskenpflicht nach gesetzl. Regelung; regional gilt FFP2-Maskenpflicht",
                "providerCode": "PF",
                "type": "Timetable",
                "properties": {
                    "subnet": "ddb"
                }
            },
            {
                "content": "Linie S1: Im Zug gilt bundesweit 3G-Regel: ein gültiger Nachweis ist mitzuführen",
                "providerCode": "Y3G",
                "type": "Timetable",
                "properties": {
                    "subnet": "ddb"
                }
            },
            {
                "content": "Linie S1: Fahrradmitnahme begrenzt möglich",
                "providerCode": "FB",
                "type": "Timetable",
                "properties": {
                    "subnet": "ddb"
                }
            },
            {
                "content": "Linie S1: Fahrzeuggebundene Einstiegshilfe vorhanden",
                "providerCode": "EH",
                "type": "Timetable",
                "properties": {
                    "subnet": "ddb"
                }
            },
            {
                "content": "Verspätung eines vorausfahrenden Zuges",
                "providerCode": "ddb92E01_R_IncidentCall633_20005194_1",
                "type": "RTIncidentCall",
                "properties": {
                    "subnet": "ddb"
                }
            }
        ],
        "properties": {
            "AVMSTripID": "31124-800337-8000080-141100"
        }
    }
    stop = Stop(stop_data)
    print(stop)
