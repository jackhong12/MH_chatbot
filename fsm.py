from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_message, send_button_message, newButtonTest


class TocMachine(GraphMachine):
    def __init__(self):
        #----------------------------------------------------------------------------------
        #dfa all state
        dfa = {
            'states': [
                'user',
                'menu',
                'order',
                'hambuger',
                'addEggAddCheese',
                'noEggAddCheese',
                'addEggNoCheese',
                'noEggNoCheese',
                'drink',
                'ice',
                'sugar',
                'iceSugar',
                'showBill',
                'pay'
            ],
            'transitions': [
                {
                    'trigger': 'advance',
                    'source': [
                        'noEggNoCheese',
                        'noEggAddCheese',
                        'addEggAddCheese',
                        'addEggNoCheese'
                    ],
                    'dest': 'hambuger',
                    'conditions': 'isAnotherHambuger'
                },
                {
                    'trigger': 'advance',
                    'source': [
                        'noEggNoCheese',
                        'noEggAddCheese',
                        'addEggAddCheese',
                        'addEggNoCheese'
                    ],
                    'dest': 'drink',
                    'conditions': 'isAnotherDrink'
                },
                {
                    'trigger': 'advance',
                    'source': [
                        'noEggNoCheese',
                        'noEggAddCheese',
                        'addEggAddCheese',
                        'addEggNoCheese'
                    ],
                    'dest': 'showBill',
                    'conditions': 'isShowBill'
                },
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
        self.machine.add_transition('back', 'order', 'user')
        self.machine.add_transition('back', 'menu', 'user')
        self.machine.add_transition('advance', 'user', 'menu', conditions = 'isMenu')
        self.machine.add_transition('advance', 'user', 'order', conditions = 'isOrder')
        self.machine.add_transition('advance', 'order', 'hambuger', conditions = 'isHambuger')
        self.machine.add_transition('advance', 'order', 'drink', conditions = 'isDrink')
        self.machine.add_transition('advance', 'hambuger', 'noEggNoCheese', conditions = 'isNoEggNoCheese')
        self.machine.add_transition('advance', 'noEggNoCheese', 'addEggNoCheese', conditions = 'isAddEggNoCheese')
        self.machine.add_transition('advance', 'noEggNoCheese', 'noEggAddCheese', conditions = 'isNoEggAddCheese')
        self.machine.add_transition('advance', 'noEggNoCheese', 'addEggAddCheese', conditions = 'isAddEggAddCheese')
        self.machine.add_transition('advance', 'noEggAddCheese', 'addEggAddCheese', conditions = 'isAddEgg')
        self.machine.add_transition('advance', 'addEggNoCheese', 'addEggAddCheese', conditions = 'isAddCheese')
        self.machine.add_transition('advance', 'drink', 'sugar', conditions = 'isSugar')
        self.machine.add_transition('advance', 'drink', 'ice', conditions = 'isIce')
        self.machine.add_transition('advance', 'drink', 'iceSugar', conditions = 'isIceSugar')
        self.machine.add_transition('advance', 'ice', 'iceSugar', conditions = 'isSugar')
        self.machine.add_transition('advance', 'sugar', 'iceSugar', conditions = 'isSugar')
        self.machine.add_transition('advance', 'showBill', 'pay', conditions = 'isPay')

    def isOrder(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'order'
        return False
    
    def on_enter_order(self, event):
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "orde");
        self.back()

    def isMenu(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'menu'
        return False

    def on_enter_menu(self, event):
        sender_id = event['sender']['id']
        #responese = send_button_message(sender_id, "menu");
        responese = newButtonTest(sender_id)
        self.back();
