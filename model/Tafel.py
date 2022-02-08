from telegram import InlineKeyboardMarkup

import util
from model.Stop import Stop
from vrr.vrr_api import get_data

import vars
from util import bold, monospace, now, name_linie, italic

from parser import unparse


# verkehrsmittel speichern und beim refresh einbinden
# refresh ergibt error
class Tafel:
    name = 'Tafelname'
    stops = None
    haltestelle = ''
    names = []
    linien = []
    cmd = ''
    time = None
    richtung = ''

    def __init__(self, haltestelle, linien=None, richtung=None, verkehrsmittel=None) -> None:
        # print('init', haltestelle, linien, richtung, verkehrsmittel)
        self.haltestelle = haltestelle
        if not linien: linien = []
        self.linien = linien.copy()
        self.richtung = richtung
        self.verkehrsmittel = verkehrsmittel
        self.cmd = unparse('tafel', haltestelle, linien, richtung)
        if linien:
            self.names, linien = name_linie(linien)
            if self.richtung:
                linien = [f'{linie}:{self.richtung}' for linie in linien]
        response = get_data(haltestelle, linien, verkehrsmittel)
        location = response['locations'][0]
        if 'disassembledName' in location:
            self.name = location['disassembledName']
        else:
            self.name = location['name']
        if 'stopEvents' in response:
            self.getStops(response['stopEvents'])
        else:
            self.stops = ['Keine Eregbnisse für diese Suchanfrage']

    def __str__(self):
        string = f'{self.name}'
        if self.names:
            string += f' ({", ".join(self.names)})'
        if self.verkehrsmittel:
            string += f' ({self.verkehrsmittel})'
        string += f'\n{self.getStopsString()}'
        return string

    def telegram_str(self):
        string = f'{bold(self.name)}'
        if self.names:
            string += f' ({italic(", ".join(self.names))})'
        if self.verkehrsmittel:
            string += f' ({italic(self.verkehrsmittel)})'
        string += f'\n{monospace(self.getStopsString())}'
        return string

    def getStops(self, input_list: Stop) -> list:
        self.stops = []
        for stop in input_list:
            self.stops.append(Stop(stop))

    def getStopsString(self) -> str:
        return '\n'.join((str(stop) for stop in self.stops))

    def reply_markup(self):
        buttonList2 = [('refresh', unparse('t', self.haltestelle, self.linien, self.richtung, self.verkehrsmittel)),
                       ('edit', unparse('haltestelle', self.haltestelle))]
        if self.linien and not self.verkehrsmittel:
            buttonList2.append(self.direction_emoji_cmd())
        buttonList = [util.makeButton(buttonList2)]
        return InlineKeyboardMarkup(buttonList)

    def direction_emoji_cmd(self):
        # print('haltestelle:', self.haltestelle, 'linien:', self.linien)
        cmd = unparse('t', self.haltestelle, self.linien)
        if self.richtung == 'H':
            return '➡', f'{cmd} -r R'
        elif self.richtung == 'R':
            return '⬅', f'{cmd}'
        else:
            return '↔️', f'{cmd} -r H'


if __name__ == '__main__':
    linien = ['U35:bgs:32U35:', '349:bgs:34349:']
    linien = ['349:bgs:34349:']
    # tafel = Tafel('de:05911:5140',
    #               linien=['U35:bgs:32U35:'],
    #               richtung='R',
    #               verkehrsmittel=None)
    tafel = Tafel('de:05911:5140',
                  verkehrsmittel='bahn')
    # tafel = Tafel('20005696', linien)
    print(tafel)
