import lib.reader
import sys

plugs = ['']
    #add additional files with commands here
    # first '' should be a valid python variable name (alphanumeric, first char = letter)
    # second '' should be the name of the Python file in the plugins folder

for plug in plugs:
    try:
        exec('from plugins.%s import *' % plug)
    except ModuleNotFoundError:
        print('could not import module ' + plug)


def listcommands():  # lists commands from this file
    commands = []
    cmd_dict = {k: v for k, v in globals().items() if v}
    for cmd in cmd_dict:
        if not cmd.startswith('__') and cmd not in ['lib', 'sys', 'command', 'listcommands']:
            commands.append(str(cmd))

    return commands


async def quit(ws, message, room, sender):
    if sender[0] in lib.reader.admins:
        sys.exit()


async def say(ws, message, room, sender):
    text = message[-1][len(lib.reader.key)+4:]
    if sender[0] in lib.reader.admins:
        await lib.reader.send(ws, text, room)
    elif sender[2] in '@#':
        await lib.reader.send(ws, '/'+text, room)
    else:
        room = 'pm|' + sender[0]
        await lib.reader.send(ws, 'You do not have sufficient permissions to use this command.', room)


async def help(ws, message, room, sender):
    if room.startswith('pm|') or not sender[0] in lib.reader.admins or not sender[2] in '+%★☆@#':
        await lib.reader.send(ws, 'I am a bot whose Github hasn\'t been updated since initialisation :(', 'pm|'+sender[0])

    elif sender[0] in lib.reader.admins or sender[2] in '+%★☆@#':
        await lib.reader.send(ws, 'I am a bot whose Github hasn\'t been updated since initialisation :(', room)


async def Say(ws, message, room, sender):
    text = message[-1][len(lib.reader.key)+4:]
    text = text.split(',')
    print(text)
    if sender[0] in lib.reader.admins:
        await lib.reader.send(ws, text[1], text[0])


async def command(ws, message, room, cmd):
    if room.startswith('pm|'):
        sender = await lib.reader.readname(message[2])
    else:
        sender = await lib.reader.readname(message[3])
    return await globals()[cmd](ws, message, room, sender)
