class Linie:
    name = ''
    id = ''
    cmd = ''
    haltestelle = None

    def __init__(self, haltestelle, response):
        if 'disassembledName' in response:
            self.name = response['disassembledName']
        else:
            self.name = response['name']
        self.id = response['id'].split()[0]
        self.haltestelle = haltestelle
        self.cmd = f'add {haltestelle} -a {self.name}:{self.id}'

    def __str__(self):
        return f'{self.name} {self.id}'
