import random
import asyncio
from discord.ext import commands

class guess(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("guess cog loaded")

    @commands.command()
    async def guess(self, message):
        await message.channel.send('Guess a number between 1 and 10.')

        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        answer = random.randint(1, 10)
        try:
          guess = await self.client.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send(f'Sorry, you took too long it was {answer}.')
        if int(guess.content) == answer:
            m = await message.channel.send('You are right! Lots of chocolate for you')
            await m.add_reaction('🍫')
        else:
            msg = await message.channel.send(f'Oops. It is actually {answer}.')
            await msg.add_reaction('🤔')
def setup(client):
    client.add_cog(guess(client))