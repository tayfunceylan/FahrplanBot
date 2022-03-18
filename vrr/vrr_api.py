import requests


def get_linien(id):
    url = 'https://www.vrr.de/vrr-efa/XML_SERVINGLINES_REQUEST'
    payload = {
        'language': 'de',
        'lineReqType': 1,
        'mergeDir': 'true',
        'mode': 'odv',
        'name_sl': id,
        'outputFormat': 'rapidJSON',
        'serverInfo': 1,
        'type_sl': 'stop',
    }
    req = requests.get(url, payload)
    return req.json()['lines']


def get_data(id, linien, verkehrsmittel=None):
    # U-Bahn: 2, Straßenbahn: 3, 4, Bus: 5, 6, 7, 19, Sonstige: 8, 9, 10, 11, 12, 17, Zug: 0, 13, 18, S-Bahn: 1
    # ICE: 16, IC / EC: 14, 15
    bus = [5, 6, 7, 19]
    bahn = [2, 3, 4]
    verkehrmittel_filter = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19]
    if verkehrsmittel == 'bus':
        verkehrmittel_filter = bus
        linien = None
    elif verkehrsmittel == 'bahn':
        verkehrmittel_filter = bahn
        linien = None
    url = 'https://www.vrr.de/vrr-efa/XML_DM_REQUEST'
    payload = {
        'deleteAssignedStops_dm': 1,
        'depSequence': 3,
        'depType': 'stopEvents',
        'doNotSearchForStops': 1,
        'genMaps': 0,
        'imparedOptionsActive': 0,
        'includeCompleteStopSeq': 0,
        'includedMeans': 'checkbox',
        'itOptionsActive': 1,
        'language': 'de',
        'line': linien,
        'locationServerActive': 1,
        'maxTimeLoop': 1,
        'mode': 'direct',
        'name_dm': id,
        'outputFormat': 'rapidJSON',
        'ptOptionsActive': 1,
        'type_dm': 'any',
        'useAllStops': 1,
        'useElevationData': 1,
        'useProxFootSearch': 0,
        'useRealtime': 1,
        'vrrDMMacro': 1
    }
    for inclMotNo in verkehrmittel_filter:
        payload[f'inclMOT_{inclMotNo}'] = True
    req = requests.get(url, payload)
    return req.json()


def search(searchString):
    url = "https://openservice-test.vrr.de/static02/XML_STOPFINDER_REQUEST"

    querystring = {"language": "de", "name_sf": "bochum", "outputFormat": "rapidJSON", "type_sf": "any",
                   "vrrStopFinderMacro": "1"}

    req = requests.get(url, params=querystring)
    return req.json()['locations']


if __name__ == '__main__':
    print(search('Bochum'))
