import requests
from bs4 import BeautifulSoup

class MHCrawler():
    officialWeb = {
        'quest':'.quest',
        'title':'.title',
    };
    wikiWeb = {
    };
    urlWeb = {
        'official':'http://game.capcom.com/world/steam/hk/schedule.html',
        'wiki':'https://www.mhchinese.wiki/'
    };
    mbuffer = '';

    ###################################################################
    def __init__(self):
        pass
    
    def setUrl(self, select):
        self.res = requests.get(self.urlWeb.get(select), 'html.parser')
        self.soup = BeautifulSoup(self.res.text, 'html.parser')


    def listAllQuest(self):
        self.setUrl('official')
        self.mbuffer = ''
        for drink in self.soup.select('{}'.format(self.officialWeb.get('title'))):
            self.mbuffer += drink.get_text()
        print(self.mbuffer)


    def searchQuest(self):
        setUrl('official')
        self.mbuffer = ''
        for drink in self.soup.select('{}'.format(self.officialWeb.get('quest'))):
            self.mbuffer += drink.get_text()
            self.mbuffer += "-------------------------------------"
        print(self.mbuffer)



if __name__ == "__main__":
    mhc = MHCrawler()
    mhc.listAllQuest()
