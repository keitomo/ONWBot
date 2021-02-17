class Human():
    def __init__(self,name="human",team="none",forecast="none"):
        self.name=name
        self.team=team
        self.forecast=forecast

class Villager(Human):
    def __init__(self, name='村人', team='村', forecast='村人'):
        super().__init__(name=name, team=team, forecast=forecast)

class Seer(Human):
    def __init__(self, name='占い師', team='村', forecast='村人'):
        super().__init__(name=name, team=team, forecast=forecast)

class Thief(Human):
    def __init__(self, name='怪盗', team='村', forecast='怪盗'):
        super().__init__(name=name, team=team, forecast=forecast)

class Werewolf(Human):
    def __init__(self, name='人狼', team='狼', forecast='人狼'):
        super().__init__(name=name, team=team, forecast=forecast)

class Madman(Human):
    def __init__(self, name='狂人', team='狼', forecast='村人'):
        super().__init__(name=name, team=team, forecast=forecast)

class Punishment(Human):
    def __init__(self, name='吊人', team='吊人', forecast='吊人'):
        super().__init__(name=name, team=team, forecast=forecast)

class OneNightWolf:
    def __init__(self):
        self.time=0
        self.member=set()
        self.positions=[]

    def setAll(self,time=None,member=None,postions=None):
        if time != None:
            self.setTime(time=time)
        if member != None:
            self.setMember(member=member)
        if postions != None:
            self.setPostions(postions=postions)

    def setTime(self,time):
        self.time=time

    def setMember(self,member):
        self.member=member

    def setPostions(self,postions):
        self.positions=postions

    def addMember(self,user):
        self.member.add(user)

    def start(self):
        pass

    def end(self):
        pass