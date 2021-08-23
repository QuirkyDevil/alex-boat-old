import random
import discord
import secrets
from discord.ext import commands
from utils import http
from io import BytesIO
class fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("fun cog loaded")

    @commands.command()
    @commands.cooldown(1, 5)
    async def say(self, ctx, *, message: commands.clean_content()):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def flipcoin(self, ctx):
        choices = ['You fot Heads', 'You got tails']
        color = discord.Color.green()
        em = discord.Embed(color=color, title='Coin Flip:', description=random.choice(choices))
        await ctx.send(embed=em)

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command(aliases=["shoes"])
    async def throwshoes(self, ctx):
        """ Shoes go brrrr """
        bio = BytesIO(await http.get("https://media.tenor.com/images/720670aa33166a1688d2141e37cef22c/tenor.gif", res_method="read"))
        await ctx.send(file=discord.File(bio, filename="noticeme.gif"))
        await ctx.send(f"**{ctx.author.name}** gave you a gift")
    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for yo"""
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command(aliases=["slots", "bet"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")



def setup(client):
    client.add_cog(fun(client))