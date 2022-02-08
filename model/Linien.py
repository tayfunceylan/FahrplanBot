from telegram import InlineKeyboardMarkup

import util
from model.Linie import Linie
from parser import unparse
from util import reshape
from vrr.vrr_api import get_linien

import vars


class Linien:
    id = ''
    linien = None

    def __init__(self, id):
        self.id = id
        self.loadLinien()

    def loadLinien(self):
        self.linien = []
        for line in get_linien(self.id):
            self.linien.append(Linie(self.id, line))

    def reply_markup(self, fahrplan_cmd, isSelected=False):
        args = [(linie.name, linie.cmd) for linie in self.linien]
        args = list(dict.fromkeys(args))
        args = reshape(args, 5)
        buttonList = [util.makeButton(linie) for linie in args]
        if not isSelected:
            buttonList1 = [('alle Buslinien', unparse('t', self.id, verkehrsmittel='bus')),
                           ('alle Bahnlinien', unparse('t', self.id, verkehrsmittel='bahn'))]
            buttonList.append(util.makeButton(buttonList1))
        buttonList.append(util.makeButton([('zum Fahrplan', fahrplan_cmd)]))
        return InlineKeyboardMarkup(buttonList)


if __name__ == '__main__':
    x = Linien('de:05911:5696')
    x.loadLinien()
    # x.reply_markup('t de:05911:5696 U35:bgs:32U35:', 'U35:bgs:32U35:')
    x.reply_markup('t de:05911:5696', '')
