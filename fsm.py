from transitions.extensions import GraphMachine
from monsterHunterCrawler import MHCrawler
from utils import send_text_message, send_image_message, send_video_message, send_button_message

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
                'monster',
                'attackEffect',
                'video',
                'trap',
                'effect',
                'character'
                
            ],
            'transitions': [
                {
                    'trigger': 'back',
                    'source':[
                        'video',
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
                },
                {
                    'trigger': 'back',
                    'source':[
                        'attackEffect',
                        'trap',
                        'effect',
                        'character'
                    ],
                    'dest': 'monster',
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
        self.machine.add_transition('advance', 'allMonster', 'monster', conditions = 'isMonster')
        self.machine.add_transition('advance', 'monster', 'monster', conditions = 'isMonster2')
        self.machine.add_transition('advance', 'monster', 'allMonster', conditions = 'isBack')
        self.machine.add_transition('back', 'monster', 'allMonster')
        self.machine.add_transition('advance', 'monster', 'attackEffect', conditions = 'isAttackEffect')
        self.machine.add_transition('advance', 'user', 'video', conditions = 'isVideo')
        self.machine.add_transition('advance', 'monster', 'effect', conditions = 'isEffect')
        self.machine.add_transition('advance', 'monster', 'trap', conditions = 'isTrap')
        self.machine.add_transition('advance', 'monster', 'character', conditions = 'isCharacter')
        #
     
    def on_enter_character(self, event):
        sender_id = event['sender']['id']
        self.mhc.dropItem()
        responese = send_text_message(sender_id, self.mhc.monEff['character']);
        self.back(event)

    def isCharacter(self, event):
        sender_id = event['sender']['id']
        text = event['message']['text']
        if text == "特徵":
            return True
        else:
            return False

    def on_enter_trap(self, event):
        sender_id = event['sender']['id']
        self.mhc.dropItem()
        responese = send_text_message(sender_id, self.mhc.monEff['trap']);
        self.back(event)
        
    def isTrap(self, event):
        sender_id = event['sender']['id']
        text = event['message']['text']
        if text == "陷阱":
            return True
        else:
            return False

    def on_enter_effect(self, event):
        sender_id = event['sender']['id']
        self.mhc.dropItem()
        responese = send_text_message(sender_id, self.mhc.monEff['seffect']);
        self.back(event)
        
    def isEffect(self, event):
        sender_id = event['sender']['id']
        text = event['message']['text']
        if text == "效果":
            return True
        else:
            return False

    def isVideo(self, event):
        sender_id = event['sender']['id']
        text = event['message']['text']
        if text == "video":
            return True
        else:
            return False

    def on_enter_video(self, event):
        sender_id = event['sender']['id']
        responese = send_video_message(sender_id, "http://clips.vorwaerts-gmbh.de/VfE_html5.mp4");
        self.back(event)

    def isAttackEffect(self, event):
        sender_id = event['sender']['id']
        text = event['message']['text']
        if text == "弱點":
            return True
        else:
            return False

    def on_enter_attackEffect(self, event):
        sender_id = event['sender']['id']
        self.mhc.dropItem()
        responese = send_text_message(sender_id, self.mhc.monEff['weak']);
        self.back(event)

    def isMonster2(self, event):
        sender_id = event['sender']['id']
        text = event['message']['text']
        if self.mhc.searchMonster(text): 
            print(self.mhc.monImg)
            responese = send_image_message(sender_id, self.mhc.monImg)
            responese = send_text_message(sender_id, self.mhc.monster.get(1))
            #print(self.mhc.monster.get(1))
            return True
        else:
            return False

    def isMonster(self, event):
        sender_id = event['sender']['id']
        text = event['message']['text']
        if self.mhc.searchMonster(text): 
            print(self.mhc.monImg)
            responese = send_image_message(sender_id, self.mhc.monImg)
            responese = send_text_message(sender_id, self.mhc.monster.get(1))
            #print(self.mhc.monster.get(1))
            return True
        else:
            responese = send_text_message(sender_id, "請輸入正確魔物名子")
            return False


    def on_enter_monster(self, event):
        sender_id = event['sender']['id']
    
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
            responese = send_image_message(sender_id, self.mhc.murl)
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
            return text.lower() == 'command'
        return False

    def on_enter_command(self, event):
        """
        self.mhc.listAllMonster()
        self.mhc.searchMonster('滅盡龍')
        self.mhc.dropItem()
        responese = send_text_message(sender_id, self.mhc.drop.get(1))
        """
        sender_id = event['sender']['id']
        responese = send_button_message(sender_id)
        self.back()
