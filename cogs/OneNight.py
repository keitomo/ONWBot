from discord.ext import commands
import discord
import asyncio
from cogs.OneNightGame import *

MAIN_SCREEN = 0
OPTION_SCREEN = 1
COUNT_SCREEN = 2
START_SCREEN = 3
VOTE_SCREEN = 4
END_SCREEN = 5


class OneNight(commands.Cog,name="OneNight"):
    gameList={}
    screenList={}
    messageList={}
    def __init__(self,bot):
        self.bot = bot

    @commands.group(help="ワンナイト人狼に関連するコマンド")
    async def onw(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')

    @onw.command(help="ワンナイト人狼を開始します")
    async def start(self,ctx):
        guild_id = ctx.guild.id
        game = OneNightWolf()
        OneNight.gameList[guild_id]=game
        OneNight.screenList[guild_id]=MAIN_SCREEN
        game.setAll(time=5)
        mes = await ctx.send(embed=game.mainEmbed())
        await mes.add_reaction("✋")
        await mes.add_reaction("🔧")
        await mes.add_reaction("⚔️")

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        if user.bot:
            return
        if not isinstance(reaction.message.channel, discord.DMChannel):
            guild_id = reaction.message.guild.id
            game = OneNight.gameList[guild_id]
            if reaction.emoji == "✋" and OneNight.screenList[guild_id]==MAIN_SCREEN:
                await self.joinAction(reaction,user)
            elif reaction.emoji == "🔧" and OneNight.screenList[guild_id]==MAIN_SCREEN:
                await self.settingAction(reaction,user)
            elif reaction.emoji == "⚔️" and OneNight.screenList[guild_id]==MAIN_SCREEN:
                await reaction.message.clear_reactions()
                if game.setPosition():
                    await self.setGame(guild_id,reaction.message.channel)
                else:
                    await reaction.message.channel.send("メンバーの不足、または役職の数が合わないためにゲームを始められません。")
                    await self.backAction(reaction,user)
            elif reaction.emoji == "⬅️":
                await self.backAction(reaction,user)
            elif OneNight.screenList[guild_id]==OPTION_SCREEN and reaction.emoji in ["🧑","🧙‍♀️","🕵️","🐺","🤡","👻"]:
                await self.optionAction(reaction,user)
            elif OneNight.screenList[guild_id]==COUNT_SCREEN and reaction.emoji in ["⬆️","⬇️"]:
                await self.countAction(reaction,user)
            elif reaction.emoji == "🗳️" and OneNight.screenList[guild_id]==START_SCREEN:
                await self.voteAction(reaction,user)
            elif reaction.emoji == "🔄" and OneNight.screenList[guild_id]==END_SCREEN:
                await self.resetGame(reaction,user)
        else:
            if reaction.emoji in ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]:
                try:
                    game = OneNight.messageList[reaction.message.id]
                    if game.voteMode:
                        await self.voteProc(reaction,user)
                    elif game.getPosition(user.id) == "Seer" and reaction.emoji in ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]:
                        await self.seerAction(reaction,user)
                    elif game.getPosition(user.id) == "Thief" and reaction.emoji in ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]:
                        await self.thiefAction(reaction,user)
                except KeyError:
                    pass

    async def joinAction(self,reaction,user):
        guild_id = reaction.message.guild.id
        game = OneNight.gameList[guild_id]
        game.addMember(user)
        await reaction.message.edit(embed=game.mainEmbed())

    async def backAction(self,reaction,user):
        guild_id = reaction.message.guild.id
        game = OneNight.gameList[guild_id]
        if OneNight.screenList[guild_id]==OPTION_SCREEN or OneNight.screenList[guild_id]==MAIN_SCREEN:
            await reaction.message.clear_reactions()
            OneNight.screenList[guild_id]=MAIN_SCREEN
            await reaction.message.edit(embed=game.mainEmbed())
            await reaction.message.add_reaction("✋")
            await reaction.message.add_reaction("🔧")
            await reaction.message.add_reaction("⚔️")
        elif OneNight.screenList[guild_id]==COUNT_SCREEN:
            await reaction.message.clear_reactions()
            OneNight.screenList[guild_id]=OPTION_SCREEN
            await reaction.message.edit(embed=game.settingEmbed())
            for react in ["⬅️","🧑","🧙‍♀️","🕵️","🐺","🤡","👻"]:
                await reaction.message.add_reaction(react)
        else:
            pass

    async def settingAction(self,reaction,user):
        guild_id = reaction.message.guild.id
        game = OneNight.gameList[guild_id]
        await reaction.message.clear_reactions()
        OneNight.screenList[guild_id]=OPTION_SCREEN
        await reaction.message.edit(embed=game.settingEmbed())
        for react in ["⬅️","🧑","🧙‍♀️","🕵️","🐺","🤡","👻"]:
            await reaction.message.add_reaction(react)

    async def optionAction(self,reaction,user):
        guild_id = reaction.message.guild.id
        game = OneNight.gameList[guild_id]
        target = OneNight.getID(reaction.emoji)
        await reaction.message.clear_reactions()
        OneNight.screenList[guild_id]=COUNT_SCREEN
        await reaction.message.edit(embed=game.optionEmbed(target))
        await reaction.message.add_reaction("⬅️")
        await reaction.message.add_reaction("⬆️")
        await reaction.message.add_reaction("⬇️")

    async def countAction(self,reaction,user):
        guild_id = reaction.message.guild.id
        game = OneNight.gameList[guild_id]
        target = OneNight.getID(reaction.message.embeds[0].fields[0].name)
        if reaction.emoji == "⬆️":
            game.addPosition(target)
        elif reaction.emoji == "⬇️":
            game.delPosition(target)
        await reaction.message.edit(embed=game.optionEmbed(target))
        await reaction.remove(user)

    async def voteAction(self,reaction,user):
        guild_id = reaction.message.guild.id
        game = OneNight.gameList[guild_id]
        game.voteMode = True
        OneNight.screenList[guild_id]=VOTE_SCREEN
        for member in game.member:
            if member.dm_channel == None:
                await member.create_dm()
            message = await member.dm_channel.send(embed=game.vote(member))
            OneNight.messageList[message.id]=game
            numbers=["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            for i in range(len(game.member)-1):
                await message.add_reaction(numbers[i])
            game.waitCount += 1
        embed = discord.Embed(title="ワンナイト人狼",description="投票を行ってください")
        embed.add_field(name="投票は",value="個人のDMに送付しました")
        await reaction.message.edit(embed=embed)
        while game.waitCount!=0:
            await asyncio.sleep(1)
        if  game.waitCount==0:
            await self.endGame(reaction)

    async def voteProc(self,reaction,user):
        message = reaction.message
        game = OneNight.messageList[message.id]
        del OneNight.messageList[message.id]
        await message.edit(embed=game.voteProc(user,reaction.emoji))
        game.waitCount -= 1

    async def setGame(self,guild_id,channel):
        game = OneNight.gameList[guild_id]
        for member in game.member:
            if member.dm_channel == None:
                await member.create_dm()
            try:
                message = await member.dm_channel.send(embed=game.createDM(member))
            except discord.errors.Forbidden:
                await channel.send(member.mention+"さんへDMが送信できませんでした。\nアカウントの設定の確認をお願いします。")
                continue
            if game.getPosition(member.id) =="Seer" or game.getPosition(member.id) =="Thief":
                OneNight.messageList[message.id]=game
                game.waitCount += 1
                numbers=["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
                for i in range(len(game.member)):
                    await message.add_reaction(numbers[i])
        async with channel.typing():
            while game.waitCount!=0:
                await asyncio.sleep(1)
            if  game.waitCount==0:
                await asyncio.sleep(5)
                await self.startGame(guild_id,channel)

    async def startGame(self,guild_id,channel):
        game = OneNight.gameList[guild_id]
        OneNight.screenList[guild_id]=START_SCREEN
        message = await channel.send(embed=game.start())
        await message.add_reaction("🗳️")

    async def endGame(self,reaction):
        resultmes = await reaction.message.channel.send("結果が出ました！")
        async with reaction.message.channel.typing():
            await asyncio.sleep(3)
        await resultmes.delete()
        guild_id = reaction.message.guild.id
        game = OneNight.gameList[guild_id]
        OneNight.screenList[guild_id]=END_SCREEN
        await reaction.message.edit(embed=game.end())
        await reaction.message.clear_reactions()
        await reaction.message.add_reaction("🔄")

    async def resetGame(self,reaction,user):
        message = reaction.message
        guild_id = message.guild.id
        game = OneNight.gameList[guild_id]
        game.reset()
        OneNight.screenList[guild_id]=MAIN_SCREEN
        mes = await message.channel.send(embed=game.mainEmbed())
        await mes.add_reaction("✋")
        await mes.add_reaction("🔧")
        await mes.add_reaction("⚔️")

    async def seerAction(self,reaction,user):
        game = OneNight.messageList[reaction.message.id]
        del OneNight.messageList[reaction.message.id]
        game.waitCount -= 1
        await reaction.message.edit(embed=game.getSeer(reaction.emoji))

    async def thiefAction(self,reaction,user):
        game = OneNight.messageList[reaction.message.id]
        del OneNight.messageList[reaction.message.id]
        game.waitCount -= 1
        await reaction.message.edit(embed=game.getThief(user,reaction.emoji))


    @staticmethod
    def getID(emoji):
        target = -1
        if emoji == "🧑":
            target = 0
        elif emoji == "🧙‍♀️":
            target = 1
        elif emoji == "🕵️":
            target = 2
        elif emoji == "🐺":
            target = 3
        elif emoji == "🤡":
            target = 4
        elif emoji == "👻":
            target = 5
        return target

def setup(bot):
    bot.add_cog(OneNight(bot))
