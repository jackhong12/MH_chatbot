import requests
import sys
from bs4 import BeautifulSoup

class MHCrawler():
    officialWeb = {
        'quest':'.quest',   #詳細任務
        'title':'.title',   #任務名
    };
    wikiWeb = {
        'tip':'.tip',   #魔物名
        'describe':'col-xs-12 col-sm-6',    #魔物簡介
    };
    urlWeb = {
        'official':'http://game.capcom.com/world/steam/hk/schedule.html',
        'wiki':'https://www.mhchinese.wiki/'
    };
    mbuffer = ''
    monDict = {}
    ###################################################################
    def __init__(self):
        pass
    
    def setUrl(self, select):
        self.res = requests.get(self.urlWeb.get(select), 'html.parser')
        self.soup = BeautifulSoup(self.res.text, 'html.parser')

    def chFind(self, str1, str2):
        if str1.find(str2) != -1:
            return True
        return False

    def listAllQuest(self):
        self.setUrl('official')
        self.mbuffer = '*本周任務：*\n'
        for drink in self.soup.select('{}'.format(self.officialWeb.get('title'))):
            self.mbuffer += drink.get_text()
        #print(self.mbuffer)


    def searchQuest(self, quest):
        self.setUrl('official')
        self.mbuffer = ''
        for drink in self.soup.select('{}'.format(self.officialWeb.get('quest'))):
            if self.chFind(drink.get_text(), quest):
                self.mbuffer = drink.get_text()
                return True
        return False

    def listAllMonster(self):
        self.setUrl('wiki')
        self.mbuffer = ''
        self.monDict.clear()
        for drink in self.soup.select('{}'.format(self.wikiWeb.get('tip'))):
            self.mbuffer += drink.get_text() + "\n"
            self.monDict[drink.get_text()] = drink.get('href')

    def searchMonster(self, name):
        if self.monDict.get(name):
            url = self.urlWeb.get('wiki') + self.monDict.get(name)
            print(url)
            self.setUrl("https://www.mhchinese.wiki/monsters/5a6be43094be105e619df8a0")
            """
            self.mbuffer = ''
            for drink in self.soup.select('{}'.format(self.wikiWeb.get('describe'))):
                print(drink.get_text()) 
            """
            return True
        else: 
            return False

if __name__ == "__main__":
    mhc = MHCrawler()
    mhc.listAllMonster()
    print(mhc.searchMonster('炎王龍'))
