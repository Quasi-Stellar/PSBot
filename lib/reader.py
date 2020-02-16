import requests
import json
import sys
from datetime import datetime

from lib.commands import *
from main import username, password, avatarid, init_rooms, key, roomlevels, admins, bot_msg, console_logging, logging, log_to


users = []
rooms = []
commands = listcommands()
print(commands)
showjoins = False


async def read(ws, message):
    global users, rooms
    await log(message)
    message = message.split('|')
    if len(message) == 1:
        message.append('')
    if message[1] == 'challstr':
        data = {'act': 'login',
                'name': username,
                'pass': password,
                'challstr': message[2] + '%7C' + message[3]
                }
        r = requests.post(url='https://play.pokemonshowdown.com/action.php', data=data)
        try:
            r = json.loads(r.text[1:])
        except json.decoder.JSONDecodeError:
            print('missing or broken value (most likely password)!')

        await send(ws, '/trn %s,0,%s' % (username, r['assertion']))
        await send(ws, '/avatar %s' % avatarid)

        ## [ optional setting ] ##
        await send(ws, '/bch')

        for room in init_rooms:
            await send(ws, '/j %s' % room)

        print('connected as '+username)

    if message[1] == 'init':
        rooms.append(message[0][1:])
        print('joined: '+rooms[-1])
        for i in message[6].split(','):
            users.append(i)
    elif not message[1] in ['J', 'L', 'N', 'B']:
        room = message[0][1:-1]
        if message[1] == 'pm':
            room = 'pm|' + message[2]  # pm|user (Ex. pm|~Zarel, pm| QuasiStellar)
        elif message[1] == 'c:':
            message[-1] = message[-1][:-1]
        if message[-1].startswith(key) and message[-1] != key:
            # msg = str(message[-1][len(key):]+' ').split(' ', 1)
            cmd = message[-1][len(key):str(message[-1]+' ').index(' ')]
            if cmd in commands:
                try:
                    await command(ws, message, room, cmd)
                except:
                    await send(ws, 'Invalid syntax: %s%s' % (key, cmd), room)
            else:
                await send(ws, 'Invalid command: %s%s' % (key, cmd), room)

        elif message[1] == 'pm' and message[2] != ' '+username:
            await send(ws, bot_msg, room)


async def send(ws, message, room=''):
    if room.startswith('pm'):
        await ws.send('|/w %s,%s' % (room[3:], message))
    else:
        await ws.send('%s|%s' % (room, message))


async def log(message):
    global logging
    exclude = ['|challstr|', '|updatesearch|', '|error|You are already blocking']
    if not logging or message == '':
        return
    for i in exclude:
        if message.startswith(i):
            return
    if log_to == '':
        logging = False
        return
    if message.startswith('|updateuser|'):
        if message.startswith('|updateuser| Guest'):
            message = '\n\n=== NEW INSTANCE %s ===\n' % str(datetime.now())[:-7] + message[:message.index('{')]
        else:
            message = message[:message.index('}') + 1]
    elif '\n|init|chat\n' in message:
        message = message[message.index('\n|raw|<div class="infobox"> You joined'):message.index('\n|raw|<div class="infobox ')]
    else:
        await cprint(message)
    with open(log_to+'.txt', 'a') as f:
        if '\n|L|' not in message and '\n|J|' not in message:
            f.write('\n')
        f.write(message+' ')


async def cprint(message):
    global showjoins
    if console_logging:
        if showjoins:
            print(message)
        elif '\n|L|' not in message and '\n|J|' not in message:
            print(message)


async def readname(name, busy=None):
    name_ = ''
    for i in name.lower():
        if i in 'abcdefghijklmnopqrstuvwxyz1234567890':
            name_ += i

    if name[-2:] == '@!':
        busy = True

    return name_, busy, name[0]  # name, busy, auth (if any)
