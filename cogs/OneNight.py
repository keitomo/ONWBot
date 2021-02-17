from discord.ext import commands
import discord
from cogs.OneNightGame import *

class OneNight(commands.Cog,name="OneNight"):
    gameList={}
    def __init__(self,bot):
        self.bot = bot

    @commands.group(help="ワンナイト人狼に関連するコマンド")
    async def onw(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')

    @onw.command(help="コマンドグループのサブコマンド")
    async def test(self,ctx):
        """入力中
        async with ctx.channel.typing():
        """
        if ctx.author.dm_channel == None:
            await ctx.author.create_dm()
        await ctx.author.dm_channel.send("hello!")

    @onw.command(help="コマンドグループのサブコマンド")
    async def getVC(self,ctx):
        print(self.bot.voice_clients)

    @onw.command(help="ボイスに参加")
    async def joinVC(self,ctx):
        await ctx.author.voice.channel.connect()
        print(ctx.bot.voice_clients)

    @onw.command(help="ワンナイト人狼を開始します")
    async def start(self,ctx):
        guild_id = ctx.guild.id
        game = OneNightWolf()
        OneNight.gameList[guild_id]=game
        game.setAll(time=5)
        embed = discord.Embed(title="ワンナイト人狼",description="以下の状況でゲームをスタートします")
        embed.add_field(name="時間",value=str(game.time)+"分")
        embed.add_field(name="参加者",value=game.member)
        embed.add_field(name="役職",value=game.positions)
        mes = await ctx.send(embed=embed)
        await mes.add_reaction("✋")

    @commands.Cog.listener()
    #コマンドクラス事のイベント関係はここで処理する
    async def on_message(self, message):
        if message.author.bot:
            return

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        guild_id = reaction.message.guild.id
        game = OneNight.gameList[guild_id]
        if user != self.bot.user and reaction.emoji == "✋":
            game.addMember(user)
        embed = discord.Embed(title="ワンナイト人狼",description="以下の状況でゲームをスタートします")
        embed.add_field(name="時間",value=str(game.time)+"分")
        embed.add_field(name="参加者",value=game.member)
        embed.add_field(name="役職",value=game.positions)
        await reaction.message.edit(embed=embed)

def setup(bot):
    bot.add_cog(OneNight(bot))
