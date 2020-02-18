import re
import requests

import src.reader
import data.pokedex


async def check_team(ws, message, room, sender, is_admin):

    if room.startswith('pm|') or sender[2] in '+%@#' or is_admin:
        send_to = room
    else:
        send_to = 'pm|' + sender[0]

    # om, battle_room = re.split(',\s*',str(message))
    # om, battle_room = str(message).split(',', 1)
    try:
        om, battle_room = re.split(',\s*', str(message))
        # format: .check_team format [word], room
          # Ex. .check_team scrabble GARNET, battle-gen8ou-0000000001
          # Ex. .check_team chessmons, battle-gen8ubers-0000000002

    except ValueError:
        if not room.startswith('battle-gen8'):
            return await src.reader.send(ws, 'Invalid room. Room must be specified if not used in a Gen 8 battle room.', room)
        om = message
        battle_room = room
    if re.split('\s\s*', om)[0] not in ['chess', 'chessmons', 'scrab', 'scrabble', 'scrabblemons']:
        return await src.reader.send(ws, 'Invalid format. Validation not supported for %s.' % om.split(' ')[0], send_to)
    elif re.split('\s\s*', om)[0] in ['scrab', 'scrabble', 'scrabblemons']:
        if len(re.split('\s\s*', om)) != 2 or len(re.split('\s\s*', om)[1]) != 6:
            return await src.reader.send(ws, 'Given word is invalid; it should be 6 letters long.', send_to)
        elif not re.match('[a-zA-Z][a-zA-Z]*', re.split('\s\s*', om)[1]):
            return await src.reader.send(ws, 'Scrabble word should only contain letters.', send_to)
        else:
            print(len(re.split('\s\s*', om)))
            print(len(re.split('\s\s*', om)[1]))
            return

    while battle_room[-1] == ' ':
        battle_room = battle_room[:-1]

    await src.reader.send(ws, '/j ' + battle_room)
    rooms = src.reader.rooms
    while battle_room not in src.reader.rooms:
        msg = await src.reader.receive(ws)
        if msg.startswith('|noinit|'):
            break
            print('battle_room: "%s"' % battle_room)
            print('rooms: ' + str(rooms))
            return await src.reader.send(ws, 'Could not join room!', send_to)

    try:
        battle = []
        battles = src.reader.get(ws, 'battles')
        battle = battles[battle_room]
        print('Battle data: ' "%s" % str(battle))
        p1 = battle[0].split('|')[3]
        p2 = battle[1].split('|')[3]
        team1 = battle[battle.index('|clearpoke') + 1: battle.index('|clearpoke') + 7]
        team2 = battle[battle.index('|clearpoke') + 7: battle.index('|clearpoke') + 13]
        print('P1: ', p1)
        print('P2: ', p2)
        print('Team 1: ', team1)
        print('Team 2: ', team2)
        players = [await src.reader.readname(p1), await src.reader.readname(p2)]
        players = [players[i] for i in range(len(players))]
        if sender[0] not in players:
            if sender[2] not in '+%@#' and not is_admin:
                return await src.reader.send(ws, 'You do not have sufficient permissions to use this command here.', send_to)
        for i in range(6):
            if i < len(team1):
                team1[i] = await data.pokedex.clear_name(team1[i].split('|')[3].split(',', 1)[0])
            else:
                await src.reader.send(ws, '%s does not have a full team; it may be considered invalid.' % p1, battle_room)
            if i < len(team2):
                team2[i] = await data.pokedex.clear_name(team2[i].split('|')[3].split(',', 1)[0])
            else:
                await src.reader.send(ws, '%s does not have a full team; it may be considered invalid.' % p2, battle_room)
        print('Team 1:', team1)
        print('Team 2:', team2)
        teams = [team1, team2]
    except ValueError:
        return await src.reader.send(ws, 'Could not read teams. Validation only supported in games with team preview.', battle_room)

    if om == 'chess' or om == 'chessmons':
        legal = await check_chessmons(teams, ws, battle_room)
        print("'" + battle_room + "'")
        if not legal[0]:
            await src.reader.send(ws, '%s\'s team is not legal!' % p1, battle_room)
        if not legal[1]:
            await src.reader.send(ws, '%s\'s team is not legal!' % p2, battle_room)
        if legal[0] and legal[1]:
            await src.reader.send(ws, 'Both teams are legal!', battle_room)
    else:
        await src.reader.send(ws, 'Other formats not supported yet.', battle_room)
    # elif ' ' in om and om.split(' ')[0] in ['scrab', 'scrabble', 'scrabblemons']:
    #     pass  # do something

    # await src.reader.send(ws, message, room)


async def check_chessmons(teams, ws, battle_room):

    valid_kings = 0  # will count how many valid kings are in a team
    kings = ['dragonite', 'tyranitar', 'metagross', 'salamence', 'garchomp',
             'hydreigon', 'goodra', 'kommoo', 'dragapult']

    tiers = [[], []]
    evos = [[], []]
    for t in range(len(teams)):
        for poke in range(6):
            gt = await data.pokedex.get_tier(teams[t][poke])
            ge = await data.pokedex.get_evo(teams[t][poke])
            tiers[t].append(gt)
            evos[t].append(ge)
        team = teams[t]
        tier = tiers[t]
        evo = evos[t]
        pawn = ''
        knight = ''
        bishop = ''
        rook = ''
        queen = ''
        king = ''
        # find pawn
        if 'LC' in tier:
            pawn = team[tier.index('LC')]
            # find knight
            for poke in team:
                if poke in evo[tier.index('LC')]:
                    knight = poke
            if not knight or tier[team.index(knight)] == 'Uber':
                pass
                # something about invalid
            else:
                ind = team.index(pawn)
                del team[ind], tier[ind], evo[ind]
                ind = team.index(knight)
                del team[ind], tier[ind], evo[ind]

        else:
            print('invalid')  # some message about needing a pawn

        # find bishop
        print(tier)
        print(evo)
        for poke in team:
            if poke in kings:
                valid_kings += 1
            if tier[team.index(poke)] not in ['OU', 'Uber', 'Illegal']:
                if poke not in kings or valid_kings > 1:
                    bishop = poke
                    if poke in kings:
                        valid_kings -= 1
                    ind = team.index(poke)
                    del team[ind], tier[ind], evo[ind]
                    break
        print(team)
        # find rook
        for poke in team:
            if tier[team.index(poke)] not in ['Uber', 'Illegal']:
                if poke not in kings or valid_kings > 1:
                    rook = poke
                    if poke in kings:
                        valid_kings -= 1
                    ind = team.index(poke)
                    del team[ind], tier[ind], evo[ind]
                    break
        for poke in team:
            if tier[team.index(poke)] not in ['Illegal']:
                if poke not in kings or valid_kings > 1:
                    queen = poke
                    if poke in kings:
                        valid_kings -= 1
                    ind = team.index(poke)
                    del team[ind], tier[ind], evo[ind]
                    break
        for poke in team:
            if tier[team.index(poke)] not in ['Uber', 'Illegal']:
                if poke in kings:
                    king = poke
                    ind = team.index(poke)
                    del team[ind], tier[ind], evo[ind]
                    break
        if len(team) > 0:
            teams[t] = False
        else:
            teams[t] = True
    return teams
