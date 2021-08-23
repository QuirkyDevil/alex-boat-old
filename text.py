from discord.ext import commands
import  asyncio

class text(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("fun cog loaded")

    @commands.command()
    async def on_message(self, message):
        if message.content.startswith('Alex!'):
            await message.reply('Hallo there! wat do you want me to do?', mention_author=True)
        if message.content.startswith('is kath dumb?'):
            await message.reply('she is.. (not) till the time', mention_author=True)
        if message.content.startswith('do you like kath'):
            await message.reply('next please', mention_author=False)
            await asyncio.sleep(3)
            await message.channel.send(f'why would you ask that?')

def setup(client):
    client.add_cog(text(client))