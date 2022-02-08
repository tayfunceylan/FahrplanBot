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
        self.estTime = stop['departureTimePlanned']
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
            diff = (est-planned).total_seconds() / 60.0
            string += f' +{int(diff)}'
        return string
