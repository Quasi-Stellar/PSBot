import requests
import re

dex = {}
loaded = False


async def clear_name(name):
    name = name.lower()
    clear = ''
    for i in name:
        if re.match('[a-z0-9]', i):
            clear += i
    return clear


async def load_dex():
    global dex, loaded

    dexdata = requests.get('https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/pokedex.js').text
    tierdata = requests.get('https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/formats-data.js').text

    dexdata = dexdata[dexdata.index('{\n') + 2: dexdata.index('};')]
    dexdata = dexdata.split('\t},\n')
    tierdata = tierdata[tierdata.index('{\n') + 2: tierdata.index('};')]
    tierdata = tierdata.split('\t},\n')

    evodex = {}
    tierdex = {}
    for i in dexdata:
        if ':' not in i:
            break
        name = i[1:i.index(':')]
        if 'evos:' in i:
            evos = i[i.index('evos:') + 8: i.index('"]', i.index('evos:'))].split('", "')
        else:
            evos = ""
        evodex[name] = evos
    for i in tierdata:
        if ':' not in i:
            break
        name = i[1:i.index(':')]
        if 'tier:' in i:
            tier = i[i.index('tier:') + 7: i.index('",', i.index('tier:'))]
        else:
            tier = 'illegal'
        tierdex[name] = tier
    for i in dexdata:
        if ':' not in i:
            break
        name = i[1:i.index(':')]
        if name in tierdex:
            dex[name] = [tierdex[name], evodex[name]]
            print(name + ' : ' + str(dex[name]))

    loaded = True


async def get_tier(pokemon):
    global dex, loaded
    pokemon = await clear_name(pokemon)
    try:
        return dex[pokemon][0]
    except KeyError:
        return 'ill'


async def get_evo(pokemon, final=True):
    global dex, loaded
    if loaded:
        try:
            pokemon = await clear_name(pokemon)
            children = dex[pokemon][1]
            if not children:
                return [pokemon]
            for c in children:
                if c and c in dex:
                    for child in dex[c][1]:
                        if child:
                            children.append(child)
                            children.remove(c)
                if not c:
                    children.remove(c)

            return children

        except KeyError:
            return 'KeyError'
    else:
        return 'Dex not loaded'
