from telegram import InlineKeyboardMarkup

import util
import vars
from model.Haltestelle import Haltestelle
from vrr.vrr_api import search


class Search:
    haltestellen = None

    def __init__(self, searchString):
        self.haltestellen = []
        for haltestelle in search(searchString):
            self.haltestellen.append(Haltestelle(haltestelle))

    def __str__(self):
        return '\n'.join([str(haltestelle) for haltestelle in self.haltestellen])

    def __repr__(self):
        return self.__str__()

    def select(self, selection):
        return [haltestelle for haltestelle in self.haltestellen if haltestelle.id == selection][0]

    def reply_markup(self):
        buttonList = [util.makeButton(((haltestelle.name, haltestelle.cmd),)) for haltestelle in self.haltestellen[:3]]
        return InlineKeyboardMarkup(buttonList) if buttonList else None
