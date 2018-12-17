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
    murl = ''
    monDict = {}
    monster = {}
    drop = {}
    monEff = {}
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
        i = 0
        flag = False
        for drink in self.soup.select('{}'.format(self.officialWeb.get('quest'))):
            i += 1
            if self.chFind(drink.get_text(), quest):
                self.mbuffer = drink.get_text()
                flag = True
                break
        j = 0
        for drink2 in self.soup.select('{}'.format('.image')):
            j += 2
            if j == 2*i:
                urls = drink2.findAll('img')
                for url in urls:
                    self.murl = url['src']
                break
        return flag

    def listAllMonster(self):
        self.setUrl('wiki')
        self.mbuffer = '*魔物:*\n'
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
        self.monEff.clear()
        i = 0
        for drink in self.soup.select('{}'.format(".simple-table")):
            i+=1
            self.drop[i] = drink.get_text()
            #print("\n\n---------------\n\n")
            #print(drink.get_text())
        
        #魔物弱點
        strw = self.drop.get(1)
        weakPoint = "*魔物弱點*\n"
        if len(strw) > 40:
            weakPoint = weakPoint + "斬： " + strw[26] + "\n打： " + strw[28] + "\n彈： " + strw[30] + "\n火： " + strw[32] + "\n水： " + strw[34] + "\n雷： " + strw[36] + "\n冰: " + strw[38] + "\n龍： " + strw[40] + "\n\n◎＞○＞△＞×＞無効，斬/打/彈的弱點以左邊為最有效"
        else:
            weakPoint = "none \n\n 請收尋別的魔物或資料"
        self.monEff['weak'] = weakPoint

        #狀態異常效果
        st = self.drop.get(3).replace('\n', '')
        specialEffect = ""
        if len(st) > 31:
            specialEffect = "*狀態異常效果*\n" + st[12] + ": " + st[13] + "\n"
            for i in range(14, 29, 3):
                specialEffect += st[i:i+2] + ": " + st[i+2] + "\n"
            specialEffect += "\n◎＞○＞△＞×＞無効，斬/打/彈的弱點以左邊為最有效"
        else:
            specialEffect = "none \n\n 請收尋別的魔物或資料"
        self.monEff['seffect'] = specialEffect

        #陷阱效果
        st = self.drop.get(4).replace('\n', '')
        trap = ""
        if len(st) > 39:
            trap = "*陷阱效果*\n" + st[14:18] + ": " + st[18] + "\n" + st[19:23] + ": " + st[23] + "\n"
            for i in range(24, 36, 4):
                trap += st[i:i+3] + ": " + st[i+3] + "\n" 
            trap += "\n◎＞○＞△＞×＞無効，斬/打/彈的弱點以左邊為最有效"
        else:
            trap = "none \n\n 請收尋別的魔物或資料"
        self.monEff['trap'] = trap

        #魔物特徵
        st = self.drop.get(5).replace('\n', '')
        character = ""
        if len(st) > 25:
            character = "*魔物特徵*\n" + "咆哮: " + st[20] + "\n" + "風壓: " + st[21] + "\n" + "震地: "+ st[22] + "\n" + "拘束: " + st[23] + "\n" + "属性狀態: " + st[24] + "\n" + "狀態異常: " + st[25]
        else:
            character = "none \n\n 請收尋別的魔物或資料"
        self.monEff['character'] = character
    
        #print(character)
        
        #st = self.drop.get(6).replace('\n', '')
        #print(st)

if __name__ == "__main__":
    mhc = MHCrawler()
    mhc.listAllMonster()
    #print(mhc.mbuffer)
    mhc.searchMonster('雌火龍')
    mhc.dropItem()
    #print(mhc.drop.get(2))
    #mhc.listAllQuest()
    #print(mhc.mbuffer)
    #mhc.searchQuest('兩位女王')
    #print(mhc.murl)
    print(mhc.monEff['weak'])
