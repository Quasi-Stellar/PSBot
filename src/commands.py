import sys

import src.reader
from data.pokedex import get_evo


plugs = ['validator']
# plugs = ['plug1', 'plug2']
# plugs = { 'plug2': 'plug1'
#
#            }
            # add additional files with commands here
            # first '' should be a valid python variable name (alphanumeric, first char = letter)
            # second '' should be the name of the Python file in the plugins folder
            #
for plug in plugs:
    try:
        exec('from plugins.%s import *' % plug)
    except ModuleNotFoundError:
        print('could not import module ' + plug)


def listcommands():  # lists commands from this file
    commands = []
    cmd_dict = {k: v for k, v in globals().items() if v}
    for cmd in cmd_dict:
        if not cmd.startswith('__') and cmd not in ['src', 'command', 'data', 'sys', 're', 'listcommands']:
            commands.append(str(cmd))

    return commands


async def say(ws, message, room, sender, is_admin):
    if is_admin:
        await src.reader.send(ws, message, room)
    elif sender[2] in '@#':
        if message[0] in ['/', '!']:
            await src.reader.send(ws, '//'+message[1:], room)
        else:
            await src.reader.send(ws, message, room)
    else:
        room = 'pm|' + sender[0]
        await src.reader.send(ws, 'You do not have sufficient permissions to use this command.', room)


async def help(ws, message, room, sender, is_admin):
    if room.startswith('pm|') or not is_admin or not sender[2] in '+%★☆@#':
        await src.reader.send(ws, 'Hello, I am a bot! You can find me on github at https://github.com/Quasi-Stellar/PSBot.', 'pm|'+sender[0])

    elif is_admin or sender[2] in '+%★☆@#':
        await src.reader.send(ws, 'Hello, I am a bot! You can find me on github at https://github.com/Quasi-Stellar/PSBot.', room)


async def Say(ws, message, room, sender, is_admin):
    text = message.split(',')
    print('admin %s said: %s' % (sender, text[0]))
    print('room: \'%s\'' % text[1])
    if is_admin:
        await src.reader.send(ws, text[1], text[0])


async def quit(ws, message, room, sender, is_admin):
    if is_admin:
        sys.exit()


async def command(ws, message, room, sender, cmd):
    while message and message.startswith(' '):
        message = message[1:]
    while message and message[-1] in [' ', '\n']:
        message = message[:-1]
    if room[-1] == '\n':
        room = room[:-1]
    admins = src.reader.admins
    if sender[0] in admins:
        is_admin = True
    else:
        is_admin = False
    return await globals()[cmd](ws, message, room, sender, is_admin)
