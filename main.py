from discord.ext import commands
import tictactoe
import asyncio
from weather import *


client = commands.Bot(command_prefix="?", intents=discord.Intents.all())
command_prefix = ''
tic_tac_toe_data = {}
client.remove_command('help')

player1 = ""
player2 = ""

turn = ""
gameOver = True

board = []
winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="trident")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready!")

@client.command()
async def help(ctx):
    em = discord.Embed(title= "Help is here! ~ alex", description= "Use ?help <command for extended Info>", colour= ctx.author.color.red())

    em.add_field(name="Leveling", value = "```shows your level and leaderboard of the server```")
    em.add_field(name="Fun", value="```8ball, flipcoin, say, reverse-text, slot, tictactoe (vs player), ttt (vs computer)```")
    em.add_field(name="Urban Dictionary", value="```The word is self explanatory```")
    em.add_field(name="guess", value="```The game of guessing numbers in between 10```")
    em.add_field(name="weather", value="```shows weather of any place```")
    em.add_field(name="Place", value="```A sub-command for TicTacToe vs player```")
    em.add_field(name="Password", value="```generates a random password for you```")
    em.add_field(name="GIF", value="```Throw shoes, and more coming soon!```")
    em.add_field(name="F", value="```You can pay respect with F```")
    await ctx.send(embed=em)


@client.command(aliases=['tic_tac_toe'])
async def ttt(ctx):
    global tic_tac_toe_data
    author: discord.User = ctx.message.author
    if tic_tac_toe_data.get(author, {'in_game': False})['in_game']:
        await author.send('You are already in a game. To end a game enter !end')
    else:
        msg = 'You have started a Tic-Tac-Toe game \n The game will end after 2 minutes of' \
              'inactivity or if you enter !end \n Would you like to go first? [Y/n]'
        await author.send(msg)
        author_data = tic_tac_toe_data[author] = {'comp_moves': [], 'user_moves': [], 'danger': None,
                                                  'danger2': None, 'in_game': True, 'round': 0}
        user_msg, game_channel = None, author.dm_channel

        def check_yn(waited_msg):
            correct_prereqs = waited_msg.channel == game_channel and author == waited_msg.author
            waited_msg = waited_msg.content.lower()
            bool_value = waited_msg in ('y', 'ye', 'yes','Yes','Y', 'Ye', 'n', 'no', 'na', 'nah', 'N', 'No', 'Na', 'Nah') or 'end' in waited_msg
            return bool_value and correct_prereqs

        def check_digit(waited_msg):
            correct_prereqs = waited_msg.channel == game_channel and author == waited_msg.author
            waited_msg = waited_msg.content
            return (waited_msg.isdigit() or 'end' in waited_msg.lower()) and correct_prereqs

        while user_msg is None and author_data['in_game']:
            try:
                user_msg = await client.wait_for('message', timeout=120, check=check_yn)
                if user_msg:
                    user_msg = user_msg.content.lower()
                    if 'end' in user_msg:
                        author_data['in_game'] = False
                        await author.send('You have ended your tic-tac-toe game')
                    else:
                        author_data['round'] = 1
                        temp_msg = tictactoe.greeting(author_data, user_msg)  # msg is y or n
                        await author.send(temp_msg)
            except asyncio.TimeoutError:
                author_data['in_game'] = False
        while author_data['in_game']:
            try:
                user_msg = await client.wait_for('message', timeout=120, check=check_digit)
                if user_msg is not None:
                    if 'end' in user_msg.content.lower():
                        author_data['in_game'] = False
                        await author.send('You have ended your tic-tac-toe game')
                    else:
                        player_move = int(user_msg.content)

                        temp_msg = tictactoe.valid_move(player_move, author_data)
                        if not temp_msg: await author.send('That was an invalid move')
                        else:
                            temp_msg += '\n'
                            tempt = tictactoe.tic_tac_toe_move(author_data)
                            if not author_data['in_game']:
                                if author_data['round'] == 5:
                                    await author.send(f'Your Move{temp_msg + tempt}')
                                else: await author.send(f'Your Move{temp_msg}My Move{tempt}')
                            else:
                                await author.send(f'Your Move{temp_msg}My Move{tempt}\nEnter your move (#)')
                            author_data['round'] += 1
            except asyncio.TimeoutError:
                author_data['in_game'] = False



client.load_extension('text')
client.load_extension('tictactoevsplayer')
client.load_extension('guess')
client.load_extension('urban')
client.load_extension('levels')
client.load_extension('fun')
client.load_extension('eightball')
client.run('')
