import requests
import sys
from bs4 import BeautifulSoup

class MHCrawler():
    officialWeb = {
        'quest':'.quest',   #"詳細任務"
        'title':'.title',   #"任務名"
    };
    wikiWeb = {
        'tip':'.tip',   #"魔物名"
        'des':'.col-xs-12 col-sm-6',    #"魔物簡介"
        'row':'.row',
        'item':'.item',
    };
    urlWeb = {
        'official':'http://game.capcom.com/world/steam/hk/schedule.html',
        'wiki':'https://www.mhchinese.wiki/'
    };
    mbuffer = ''
    monDict = {}
    monster = {}
    drop = {}
    ###################################################################
    def __init__(self):
        pass
    
    def setUrl(self, select):
        self.res = requests.get(self.urlWeb.get(select), 'html.parser')
        self.soup = BeautifulSoup(self.res.text, 'html.parser')
    
    def setByUrl(self, url):
        self.res = requests.get(url, 'html.parser')
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
        self.mbuffer = '*魔物:*'
        self.monDict.clear()
        for drink in self.soup.select('{}'.format(self.wikiWeb.get('tip'))):
            self.mbuffer += drink.get_text() + "\n"
            self.monDict[drink.get_text()] = drink.get('href')


    def searchMonster(self, name):
        if self.monDict.get(name):
            url = self.urlWeb.get('wiki') + self.monDict.get(name)
            #print(url)
            self.setByUrl(url)
            self.mbuffer = ''
            #print(self.soup.get_text())
            self.monster.clear()
            i = 0
            for drink in self.soup.select('{}'.format(self.wikiWeb.get("row"))):
                i+=1
                self.monster[i] = drink.get_text()
            
            #image
            images = self.soup.findAll('img')
            i = 0
            for image in images:
                if i==1:
                    self.monImg = self.urlWeb.get('wiki') + image['src']
                    #print(self.monImg)
                i+=1
                    #self.monImg = 
            #print(images)

            #print(self.monster)
            return True
        else: 
            return False

    def attackEffect(self):
        text = self.monster.get(2) + "◎＞○＞△＞×＞無効"
        return text

    def dropItem(self):
        self.drop.clear()
        i = 0
        for drink in self.soup.select('{}'.format(".simple-table")):
            i+=1
            self.drop[i] = drink.get_text()
            #print("\n\n---------------\n\n")
            #print(drink.get_text())


if __name__ == "__main__":
    mhc = MHCrawler()
    print("hello")
    mhc.listAllMonster()
    #print(mhc.mbuffer)
    mhc.searchMonster('雌火龍')
    mhc.dropItem()
    print(mhc.drop.get(2))
