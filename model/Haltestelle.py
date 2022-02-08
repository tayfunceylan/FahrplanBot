from model.Linie import Linie
from vrr.vrr_api import get_linien


class Haltestelle:
    name = ''
    id = ''
    cmd = ''
    type = ''
    linien = []

    def __init__(self, response: dict):
        self.name = response['name']
        self.id = response['ref']['gid']
        self.cmd = f'haltestelle {self.id}'
        self.type = response['anyType']

    def __str__(self):
        return f'{self.name} {self.type} {self.id}'

    def loadLinien(self):
        for line in get_linien(self.id):
            self.linien.append(Linie(self.id, line))

    def getLinien(self):
        return '\n'.join([str(linie) for linie in self.linien])

    def selectLinie(self, selection):
        return [linie for linie in self.linien if linie.id == selection][0]