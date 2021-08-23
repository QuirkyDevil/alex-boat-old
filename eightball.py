import discord
import random
from discord.ext import commands

class eightball(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("eightball cog loaded")

    @commands.command(aliases=["8ball", "magicball"])
    async def eightball(self, ctx, *, question):
        responses = ['It is certain (not)',
                     'Without a doubt',
                     'You may rely on it but not on my advice',
                     'Yes definitely',
                     'As I see it, yes',
                     'Most likely',
                     'Yes',
                     'Why?',
                     'I am not answering',
                     'Outlook good',
                     'Lemme ask Kath... and she said yes!',
                     'Signs point to yes',
                     'Reply hazy try again',
                     'Better not tell you now',
                     'Cannot predict now',
                     'Don’t count on it',
                     'Outlook not so good',
                     'My soul say no',
                     'Very doubtful',
                     'No']

        message = discord.Embed(title="8 Ball", colour=discord.Colour.orange())
        message.add_field(name="Question:", value=question, inline=False)
        message.add_field(name="Answer:", value=random.choice(responses), inline=False)
        await ctx.send(embed=message)

def setup(client):
    client.add_cog(eightball(client))
