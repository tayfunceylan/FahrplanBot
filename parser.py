import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("haltestelle", type=str)
parser.add_argument("-l", "--linien", action="extend", nargs="*", type=str)
parser.add_argument("-r", "--richtung", type=str)
parser.add_argument("-v", "--verkehrsmittel", type=str)
parser.add_argument("-a", "--linieToAdd", type=str)


def parse(input_list):
    args = parser.parse_args(input_list)
    return args


def unparse(cmd, haltestelle, linien=None, richtung=None, verkehrsmittel=None):
    liste = [cmd, haltestelle]
    if linien:
        liste.append(f'-l {" ".join(linien)}')
    if verkehrsmittel:
        liste.append(f'-v {verkehrsmittel}')
    if richtung:
        liste.append(f'-r {richtung}')
    return ' '.join(liste)


if __name__ == '__main__':
    # command = 'oskar-hoffmann -l U35'
    # args = parser.parse_args(command.split())
    # print(args)
    command = ['de:05911:5140', '-a', 'U35:bgs:32U35:']
    args = parser.parse_args(command)
    print(args)
    # x = unparse('tafel', 'oskar')
    # print(x)
