from discord.ext import commands
import random
import os
import re

class GeneralCommands(commands.Cog,name="一般的なコマンド"):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(help="Botがチャット欄で鳴きます")
    async def neko(self,ctx):
        await ctx.send("にゃーん")

    @commands.command(help="計算をしてくれます。exp:/calc 1+1")
    async def calc(self,ctx,arg):
        await ctx.send(str(eval(arg)))

def setup(bot):
    bot.add_cog(GeneralCommands(bot))