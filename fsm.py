from transitions.extensions import GraphMachine
from monsterHunterCrawler import MHCrawler
from utils import send_text_message, send_image_message, send_button_message, newButtonTest


class TocMachine(GraphMachine):
    mhc = MHCrawler()

    def __init__(self):
        #----------------------------------------------------------------------------------
        #dfa all state
        dfa = {
            'states': [
                'allMission',
                'searchMission',
                'printMission',
                'user',
                'help',
                'command',
                'allMonster',
                'moster'
            ],
            'transitions': [
                {
                    'trigger': 'back',
                    'source':[
                        'help',
                        'allMission',
                        'printMission',
                        'command'
                    ],
                    'dest': 'user'
                },
                {
                    'trigger': 'advance',
                    'source':[
                        'allMonster',
                        'searchMission'
                    ],
                    'dest': 'user',
                    'conditions': 'isBack'
                }
            ],
            'initial': 'user',
            'auto_transitions': False,
            'show_conditions': True,
        }
        #----------------------------------------------------------------------------------
        self.machine = GraphMachine(
            model=self,
            **dfa
        )
        #
        self.machine.add_transition('advance', 'user', 'allMission', conditions = 'isAllMission')
        self.machine.add_transition('advance', 'user', 'searchMission', conditions = 'isSearchMission')
        #self.machine.add_transition('advance', 'searchMission', 'searchMission', conditions = 'isSearchMission')
        self.machine.add_transition('advance', 'searchMission', 'printMission')
        self.machine.add_transition('back2Search', 'printMission', 'searchMission')
        self.machine.add_transition('advance', 'user', 'help', conditions = 'isHelp')
        self.machine.add_transition('advance', 'user', 'command', conditions = 'isCommand')
        self.machine.add_transition('advance', 'user', 'allMonster', conditions = 'isAllMonster')
        self.machine.add_transition('advance', 'allMonster', 'monster')
        #
    def isAllMonster(self, event):
        if event.get("message"):
            text = event['message']['text']
            if text.lower() == '魔物':
                return True
            if text.lower() == 'monster':
                return True
            return False
        return False

    def on_enter_allMonster(self, event):
        sender_id = event['sender']['id']
        self.mhc.listAllMonster()
        responese = send_text_message(sender_id, self.mhc.mbuffer);

    def on_enter_monster(self, event):
        pass

    def isAllMission(self, event): 
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '本周任務'
        return False
        

    def on_enter_allMission(self, event):
        sender_id = event['sender']['id']
        self.mhc.listAllQuest()
        responese = send_text_message(sender_id, self.mhc.mbuffer);
        self.back()
    
    def isBack(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'back'
        return False

    def isSearchMission(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '任務'
        return False

    def on_enter_searchMission(self, event):
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, '輸入任務');

    def on_enter_printMission(self, event):
        sender_id = event['sender']['id']
        text = ''
        if event.get('message'):
            text = event['message']['text']
        else:
            responese = send_text_message(sender_id, '請輸入文字'); 
            self.back2Search(event)
            return

        if(self.mhc.searchQuest(text)): 
            responese = send_text_message(sender_id, self.mhc.mbuffer)
            self.back()
        else:
            responese = send_text_message(sender_id, '請輸入正確任務名'); 
            self.back2Search(event)


    def isHelp(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'help'
        return False
    
    def on_enter_help(self, event):
        sender_id = event['sender']['id']
        self.mhc.listAllQuest()
        text = "*Monster Hunter Chatbot*\n你可以搜尋最近活動和魔物的功略，輸入command可以的知道所有指令"
        responese = send_image_message(sender_id, 'https://img.gq.com.tw/_rs/645/userfiles/sm/sm1024_images_A1/35545/2018031643207121.jpg')
        responese = send_text_message(sender_id, text);
        self.back()

    def isCommand(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'menu'
        return False

    def on_enter_command(self, event):
        sender_id = event['sender']['id']
        #responese = send_button_message(sender_id, "menu");
        responese = newButtonTest(sender_id)
        self.back();
