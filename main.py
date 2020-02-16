import asyncio
import websockets
import sys

import lib.reader

try:
    from config.config import config
    c = config()
    username, password, avatarid, init_rooms, key, roomlevels, admins, bot_msg, console_logging, logging, log_to = \
        c['username'], c['password'], c['avatarid'], c['init_rooms'], c['key'], c['roomlevels'], c['admins'], c['bot_msg'], \
        c['console_logging'], c['logging'], c['log_to']
except:
    print('config.py is missing or broken, trying to initialise with config_example.py')
    try:
        from config.config_example import config
        c = config()
        username, password, avatarid, init_rooms, key, roomlevels, admins, bot_msg, console_logging, logging, log_to = \
            c['username'], c['password'], c['avatarid'], c['init_rooms'], c['key'], c['roomlevels'], c['admins'], \
            c['bot_msg'], c['console_logging'], c['logging'], c['log_to']
    except ModuleNotFoundError:
        print('config_example.py is missing. Please download from https://github.com/Quasi-Stellar/PSBot.')
    except ValueError:
        print(
            'config_example.py has invalid settings. A clean version is available from https://github.com/Quasi-Stellar/PSBot.')
        sys.exit()


async def connect():
    async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as websocket:   
        while True:
            message = await websocket.recv()
            await lib.reader.read(websocket, message)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(connect())
