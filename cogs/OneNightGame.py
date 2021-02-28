class Human():
    def __init__(self,name="human",team="none",forecast="none"):
        self.name=name
        self.team=team
        self.forecast=forecast

class Villager(Human):
    def __init__(self, name='村人', team='村', forecast='村人'):
        super().__init__(name=name, team=team, forecast=forecast)
        self.ID=0
        self.icon="🧑"

class Seer(Human):
    def __init__(self, name='占い師', team='村', forecast='占い師'):
        super().__init__(name=name, team=team, forecast=forecast)
        self.ID=1
        self.icon="🧙‍♀️"

class Thief(Human):
    def __init__(self, name='怪盗', team='村', forecast='怪盗'):
        super().__init__(name=name, team=team, forecast=forecast)
        self.ID=2
        self.icon="🕵️"

class Werewolf(Human):
    def __init__(self, name='人狼', team='狼', forecast='人狼'):
        super().__init__(name=name, team=team, forecast=forecast)
        self.ID=3
        self.icon="🐺"

class Madman(Human):
    def __init__(self, name='狂人', team='狼', forecast='村人'):
        super().__init__(name=name, team=team, forecast=forecast)
        self.ID=4
        self.icon="🤡"

class Punishment(Human):
    def __init__(self, name='吊人', team='吊人', forecast='吊人'):
        super().__init__(name=name, team=team, forecast=forecast)
        self.ID=5
        self.icon="👻"

from discord.ext import commands
import discord
import random
import copy

VILLAGER = 0
SEER = 1
THIEF = 2
WEREWOLF = 3
MADMAN = 4
PUNISHMENT = 5

class OneNightWolf:
    defaultPositions=[Villager(),Seer(),Thief(),Werewolf(),Madman(),Punishment()]
    def __init__(self):
        self.time=0
        self.member=set()
        self.positions=[]
        self.field=[]
        self.memberPosition={}
        self.seerList={}
        self.thiefList={}
        self.finalPosition={}
        self.waitCount = 0
        self.voteList={}
        self.voteResult={}
        self.voteMode = False
        self.startSet = False

    def setAll(self,time=None,member=None,positions=None):
        if time != None:
            self.setTime(time=time)
        if member != None:
            self.setMember(member=member)
        if positions != None:
            self.setPositions(positions=positions)

    def setTime(self,time):
        self.time=time

    def setMember(self,member):
        self.member=member

    def setPositions(self,positions):
        self.positions=positions

    def addMember(self,user):
        self.member.add(user)

    def addPosition(self,id):
        self.positions.append(id)

    def delPosition(self,id):
        if self.positions.count(id) > 0:
            self.positions.remove(id)

    def memberList(self):
        result = "だれもいません"
        for mem in self.member:
            if result == "だれもいません":
                result = mem.mention
            else:
                result += mem.mention
            result += "\n"
        return result

    def positionsList(self):
        result = "設定されていません"
        for id in self.positions:
            if result == "設定されていません":
                result = OneNightWolf.defaultPositions[id].name
            else:
                result += OneNightWolf.defaultPositions[id].name
            result += "\n"
        return result

    def mainEmbed(self):
        embed = discord.Embed(title="ワンナイト人狼",description="以下の状況でゲームをスタートします")
        #embed.add_field(name="時間",value=str(self.time)+"分")
        embed.add_field(name="参加者",value=self.memberList())
        embed.add_field(name="役職",value=self.positionsList())
        return embed

    def settingEmbed(self):
        embed = discord.Embed(title="ワンナイト人狼",description="ゲームの設定を行います")
        if not self.startSet:
            if len(self.member)==2:
                self.positions=[VILLAGER,SEER,THIEF,WEREWOLF]
            if len(self.member)==3:
                self.positions=[VILLAGER,SEER,THIEF,WEREWOLF,WEREWOLF]
            elif len(self.member)==4:
                self.positions=[VILLAGER,VILLAGER,SEER,THIEF,WEREWOLF,WEREWOLF]
            elif len(self.member)==5:
                self.positions=[VILLAGER,VILLAGER,VILLAGER,SEER,THIEF,WEREWOLF,WEREWOLF]
            elif len(self.member)==6:
                self.positions=[VILLAGER,VILLAGER,VILLAGER,SEER,THIEF,WEREWOLF,WEREWOLF,MADMAN]
            elif len(self.member)==7:
                self.positions=[VILLAGER,VILLAGER,VILLAGER,SEER,THIEF,WEREWOLF,WEREWOLF,MADMAN,PUNISHMENT]
            elif len(self.member)>=8:
                self.positions=[VILLAGER,VILLAGER,VILLAGER,VILLAGER,SEER,THIEF,WEREWOLF,WEREWOLF,MADMAN,PUNISHMENT]
            self.startSet=True

        result = ""
        for defpos in OneNightWolf.defaultPositions:
            result += defpos.icon
            result += "："+defpos.name+" "
            result += str(self.positions.count(defpos.ID))+"人"
            result += "\n"
        embed.add_field(name="人数を変えたい役職を選んでください",value=result)
        return embed

    def optionEmbed(self,id):
        embed = discord.Embed(title="ワンナイト人狼",description="役職の人数を変えます")
        targetPos = OneNightWolf.defaultPositions[id]
        result = ""
        result += targetPos.name
        result += "："
        result += str(self.positions.count(id))+"人"
        embed.add_field(name=targetPos.icon,value=result)
        return embed

    def setPosition(self):
        if len(self.member) < 0  or len(self.member) > 10 or len(self.member)+2 != len(self.positions):
            return False
        self.field = copy.deepcopy(self.positions)
        for member in self.member:
            random.seed()
            rand = random.randrange(len(self.field))
            self.memberPosition[member]=self.field.pop(rand)
        self.finalPosition=self.memberPosition.copy()
        return True

    def getPosition(self,userid):
        member = None
        for mem in self.member:
            if mem.id == userid:
                member = mem
                break
        return OneNightWolf.defaultPositions[self.memberPosition[member]].__class__.__name__

    def getSeer(self,number):
        member = self.seerList[number]
        result = ""
        if member != "場":
            embed = discord.Embed(title="ワンナイト人狼",description=member.mention+"を占いました")
            result += OneNightWolf.defaultPositions[self.memberPosition[member]].forecast
        else:
            embed = discord.Embed(title="ワンナイト人狼",description=member+"を占いました")
            for i in range(len(self.field)):
                f=self.field[i]
                result +=OneNightWolf.defaultPositions[f].forecast
                if i != len(self.field)-1:
                    result += " と "
        embed.add_field(name="結果は・・・",value=result+"でした")
        return embed

    def getThief(self,my,number):
        member = self.thiefList[number]
        result = ""
        if member != "交換しない":
            embed = discord.Embed(title="ワンナイト人狼",description=member.mention+"の役職を奪いました")
            result += OneNightWolf.defaultPositions[self.memberPosition[member]].name+"になりました"
            temp = self.finalPosition[member]
            self.finalPosition[member] = self.finalPosition[self.thiefList[my.id]]
            self.finalPosition[self.thiefList[my.id]] = temp
        else:
            embed = discord.Embed(title="ワンナイト人狼",description="交換しませんでした")
            result = "交換しませんでした"
        embed.add_field(name="あなたは・・・",value=result)
        return embed

    def createDM(self,member):
        pos = OneNightWolf.defaultPositions[self.memberPosition[member]]
        embed = discord.Embed(title="ワンナイト人狼",description="あなたの役職はこちらです")
        embed.add_field(name=pos.icon,value=pos.name,inline=False)
        embed.add_field(name="陣営",value="あなたは"+pos.team+"陣営です",inline=False)
        if pos.__class__.__name__ == "Werewolf":
            teamMember = "いません"
            for k,v in self.memberPosition.items():
                if v == pos.ID:
                    if teamMember == "いません":
                        teamMember=k.mention
                    else:
                        teamMember+=k.mention
                    teamMember+="\n"
            embed.add_field(name="仲間",value=teamMember,inline=False)
        if pos.__class__.__name__ == "Seer":
            seerMember=""
            numbers=["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            count = 0
            seerMember += numbers[count]
            seerMember += "：場を占う"
            seerMember += "\n"
            self.seerList[numbers[count]]="場"
            count += 1
            for k,v in self.memberPosition.items():
                if k != member:
                    seerMember += numbers[count]
                    seerMember += "："+k.mention
                    seerMember += "\n"
                    self.seerList[numbers[count]]=k
                    count += 1
            embed.add_field(name="誰を占いますか？",value=seerMember,inline=False)
        if pos.__class__.__name__ == "Thief":
            self.thiefList[member.id]=member
            thiefMember=""
            numbers=["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            count = 0
            thiefMember += numbers[count]
            thiefMember += "：交換しない"
            thiefMember += "\n"
            self.thiefList[numbers[count]]="交換しない"
            count += 1
            for k,v in self.memberPosition.items():
                if k != member:
                    thiefMember += numbers[count]
                    thiefMember += "："+k.mention
                    thiefMember += "\n"
                    self.thiefList[numbers[count]]=k
                    count += 1
            embed.add_field(name="誰と交換しますか？",value=thiefMember,inline=False)
        return embed

    def start(self):
        embed = discord.Embed(title="ワンナイト人狼",description="ゲームを開始します")
        result=""
        for defpos in OneNightWolf.defaultPositions:
            result += defpos.icon
            result += "："+defpos.name+" "
            result += str(self.positions.count(defpos.ID))+"人"
            result += "\n"
        embed.add_field(name="役職一覧",value=result,inline=False)
        embed.add_field(name="投票をするには",value="以下のリアクションを押してください")
        return embed

    def vote(self,member):
        embed = discord.Embed(title="ワンナイト人狼",description="投票を行ってください")
        numbers=["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        count = 0
        result=""
        self.voteList[member]={}
        self.voteList[member][member.id]=member
        for k,v in self.memberPosition.items():
            if k != member:
                result += numbers[count]
                result += "："+k.mention
                result += "\n"
                self.voteList[member][numbers[count]]=k
                count += 1
        embed.add_field(name="誰に投票しますか？",value=result,inline=False)
        return embed

    def voteProc(self,user,number):
        member = self.voteList[user][user.id]
        votedMember = self.voteList[user][number]
        if votedMember in self.voteResult.keys():
            self.voteResult[votedMember]+=1
        else:
            self.voteResult[votedMember]=1
        embed = discord.Embed(title="ワンナイト人狼",description="投票を受け付けました")
        embed.add_field(name="あなたは",value=votedMember.mention+"さんに投票しました",inline=False)
        return embed

    def jadge(self,exeMembers):
        if len(exeMembers) == len(self.member):
            for exe in self.finalPosition.values():
                if exe == WEREWOLF:
                    return "人狼"
            return "平和村"
        for exe in exeMembers:
            if self.finalPosition[exe] == PUNISHMENT:
                return "吊り人"
        for exe in exeMembers:
            if self.finalPosition[exe] != WEREWOLF:
                return "人狼"
        for exe in exeMembers:
            if self.finalPosition[exe] == WEREWOLF:
                return "村人"
        return None

    def end(self):
        embed = discord.Embed(title="ワンナイト人狼",description="最終結果")
        voteResult = ""
        for k,v in self.voteResult.items():
            voteResult += k.mention+":"+str(v)+"票"
            voteResult += "\n"
        embed.add_field(name="投票結果",value=voteResult,inline=False)
        exeMembers = [kv[0] for kv in self.voteResult.items() if kv[1] == max(self.voteResult.values())]
        exeResult = ""
        if len(exeMembers) == len(self.member):
            embed.add_field(name="平和村・・・？",value="誰も処刑されませんでした",inline=False)
        else:
            for exe in exeMembers:
                exeResult += exe.mention + "さん"
                exeResult +="\n"
            embed.add_field(name="処刑されたのは",value=exeResult,inline=False)
        gameResult = self.jadge(exeMembers)
        if gameResult == "平和村":
            embed.add_field(name="判定は",value=gameResult+"でした",inline=False)
        else:
            embed.add_field(name="勝ったのは",value=gameResult+"陣営です",inline=False)
        resultIcon="🧑"
        if gameResult == "人狼":
            resultIcon = "🐺"
        elif gameResult == "吊り人":
            resultIcon = "👻"
        winMember = ""
        if gameResult == "人狼":
            for mem in self.member:
                if self.finalPosition[mem]==WEREWOLF or self.finalPosition[mem]==MADMAN:
                    winMember += mem.mention+"さん\n"
        elif gameResult == "吊り人":
            for mem in self.member:
                if self.finalPosition[mem]==PUNISHMENT:
                    winMember += mem.mention+"さん\n"
        else:
            for mem in self.member:
                if self.finalPosition[mem]!=WEREWOLF and self.finalPosition[mem]!=MADMAN and self.finalPosition[mem]!=PUNISHMENT:
                    winMember += mem.mention+"さん\n"
        embed.add_field(name=resultIcon,value=winMember+"おめでとうございます！",inline=False)
        procResult = ""
        for k,v in self.finalPosition.items():
            procResult+=k.mention+":"+OneNightWolf.defaultPositions[v].name
            procResult+="\n"
        embed.add_field(name="役職一覧",value=procResult,inline=False)
        return embed

    def reset(self):
        self.field=[]
        self.memberPosition={}
        self.seerList={}
        self.thiefList={}
        self.finalPosition={}
        self.waitCount = 0
        self.voteList={}
        self.voteResult={}
        self.voteMode = False
        self.startSet = False