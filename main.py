from telegram import InlineKeyboardMarkup

from model.Search import Search
from model.Tafel import Tafel
import vars


def main():
    # search for Haltestelle

    search = Search(input('Suche: '))

    # select a Haltestelle from List
    print(search)
    selection = input('Gib die ID einer Haltestelle ein: ')
    haltestelle = search.select(selection)

    # get Linien on Haltestelle
    haltestelle.loadLinien()

    # select a Line from Haltestelle
    print(haltestelle.getLinien())
    selection = input('Gib die ID einer Linie ein: ')
    linie = haltestelle.selectLinie(selection)

    # get Tafel object form Linie
    tafel = Tafel(haltestelle.id, [linie.id])
    print(tafel)

    # response = get_data()
    # test = Tafel(response)
    # print(test)


if __name__ == '__main__':
    # haltestelle = Search('Oskar Hoffmann').select('de:05911:5696')
    # haltestelle.loadLinien()
    # print(haltestelle.getLinien())
    # print(Tafel('de:05911:5696', 'bgs:32U35'))
    main()