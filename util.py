from telegram import InlineKeyboardButton

from parser import unparse, parse
from vars import ownerid
from datetime import datetime

emoji = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']


def main():
    # time1 = timeit.timeit(lambda: boldIfSame("test", 2, 2), number = 1000000)
    # time2 = timeit.timeit(lambda: boldIfSame("test", 1, 2), number = 1000000)
    # print(time1+time2)
    pass


# makes a string bold/monospace/italic
def bold(string):
    return "<b>" + string + "</b>"


def monospace(string):
    return "<code>" + string + "</code>"


def italic(string):
    return "<i>" + string + "</i>"


def bi(string):
    return bold(italic(string))


def boldIfSame(string, c):
    return bold(string) if string == c else string


def checkAdmin(userID):
    return True if userID == ownerid else False


def roleEmoji(role, dead) -> str:
    if role == 1 and dead: return '😵'
    if role == 1 and not dead:
        return '🥳'
    elif role == 2:
        return '🐺'
    return '🖐'


def intSplit(number) -> list:
    '''Splits a base 10 number into in Array of numbers between 0-9'''
    arr = []
    if number == 0:
        return [0]
    while number != 0:
        arr.insert(0, number % 10)
        number = number // 10
    return arr


def intToEmoji(number) -> str:
    '''Converts numbers to a string of Emojis'''
    arr = intSplit(abs(number))
    string = "" if number >= 0 else "-"
    for ziffer in arr:
        string += emoji[ziffer]
    return string


def now():
    return datetime.now().strftime('%H:%M')


def reshape(arr, width: int):
    lenght = len(arr)
    height = (lenght / width).__ceil__()
    return [arr[i * width:(i + 1) * width] for i in range(height)]


def name_linie(input):
    names, linien = [x.split(':', maxsplit=1)[0] for x in input], [x.split(':', maxsplit=1)[1] for x in input]
    return names, linien


def make_fahrplan(oldCmd, linieToAdd):
    cmd, *linien = oldCmd.split(' ')
    args = parse(linien)
    if not args.linien: args.linien = []
    if args.linien and linieToAdd in args.linien:
        args.linien.remove(linieToAdd)
        # print(unparse('t', args.haltestelle, args.linien))
        return unparse('t', args.haltestelle, args.linien), args.linien
    else:
        if len(args.linien) < 2:
            args.linien.append(linieToAdd)
        return unparse('t', args.haltestelle, args.linien), args.linien


def make_selection_text(selectedLinien):
    selectedLinien = [linie.split(':')[0] for linie in selectedLinien]
    selctionString = ', '.join(selectedLinien)
    return f'{bold("Linienfilter")}: {selctionString}\n(maximal 2 Linien)'


def testMakeButton():
    makeButton(['Bochum, Hustadtring', 'haltestelle de:05911:5330'])


if __name__ == '__main__':
    # x = [1,2,3,4,5,6,7,8,9]
    # y = reshape(x, 4)
    # print(y)
    # print(name_linie(['U35:bgs:32U35:', '349:bgs:34349:']))
    oldCmd = 't de:05911:5140 -l U35:bgs:32U35:'
    linieToAdd = 'U35:bgs:32U35:'
    print(make_fahrplan(oldCmd, linieToAdd))


def makeButton(text_data):
    return [InlineKeyboardButton(text=text, callback_data=data) for text, data in text_data]