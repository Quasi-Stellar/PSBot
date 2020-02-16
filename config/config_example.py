# Set the account, avatar, rooms, etc. with which the bot will start


def config():
    username = ""  # [required]
    password = ""  # [required]

    avatarid = ""  # [optional] ID for the avatar the bot should attempt to use

    init_rooms = []  # [optional] names or aliases for rooms the bot should join
		     #		  (e.g., "thehappyplace" or "thp")

    key = "+"  # the character or string for bot commands

    roomlevels = {'roomid': ['', '+', '%', '@', '#', '-'],
                  '': []
                  }
        # [not functional][optional] allows auth in different rooms access differently
        # will support in future: '' | '+' | '%' | '★' | '☆' | '@' | '#' | '&' | '~' | '-'
        # permission for each level will implied by permission given to lower levels
        # will support 6 levels: to use fewer, repeat symbols (e.g. ['','+','+','+','+','@']
          # not required, but distribution of levels may not function as intended
        # '-' will require admin permissions to this bot

    admins = []
        # [recommended] unrestricted access to commands (You!)
        # [not recommended] adding the bot may allow other users to use

    bot_msg = ('Hello! I am a bot. Type %shelp for help.' % key)
        # what bot says for random PMs
	# to set blank, change to: bot_msg = ""

    console_logging = False
        # [not recommended] if messages should be displayed in the console
        # may clutter IDE/terminal; do not turn on unless you know what you are doing

    logging = False
        # if messages should be saved and stored locally
        # will allow commands such as mail to persist across instances once implemented
        # NOTE: would not read existing logs if False

    log_to = 'chatlog'
        # [optional] must exist and not be '' to log messages
        # DO NOT include file extension (will save as .txt)

    return {'username':username,
            'password':password,
            'avatarid':avatarid,
            'init_rooms': init_rooms,
            'key':key,
            'roomlevels':roomlevels,
            'admins':admins,
            'bot_msg':bot_msg,
            'console_logging':console_logging,
            'logging':logging,
            'log_to':log_to
            }

