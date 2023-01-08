from setfit import SetFitModel
import pdb
pdb.set_trace = lambda: 1

def switch_keys_values(dictionary):
    return {value: key for key, value in dictionary.items()}

class chatBotAssistant():
    def __init__(self):
        self._load_intent_model('intent_model') 
    
    def _load_json_response(self):
        intent_map = {}
        return intent_map

    def _load_intent_model(self, weight_model):
        self.intent_model = SetFitModel.from_pretrained(weight_model)
    
    def _exit_check(self, state, user_input):
        if user_input == 'exit':
            return 1
        else:
            return state 

    def complain_response(self):
        # put message for complain
        print('do you want to complain')
        complain = input()
        # thank you for the complain
        print('thank you for feedback')
        state = 0
        return complain, state

    def menu_response(self):
        # chat the menu list
        print('here is the menu list, ayam goreng')
        state = 3
        return state  
    
    def confirm_check(self):
        print('please confirm (y/n)')
        user_confirm_order = input()
        intent = self.intent_model.predict([user_confirm_order])
        print('intent', intent)
        if intent == 5:
            flag_confirm = False
        else:
            flag_confirm = True 
        return flag_confirm

    def order_response(self, state=4, order=[]):
        order_list = []
        order_list.extend(order)
        order_confirmed = False
        print(state)
        
        if state == 4:
            state = 4
            order = []
            return order_list, state
        elif state == 3:
            while not order_confirmed:
                #bot ask what to order
                print('what to order')
                user_chat_order = input()
                state = self._exit_check(state, user_chat_order)
                if state == 1:
                    exit()
                order_list.append(user_chat_order)
                # bot confirm order
                print('confirm the order')
                order_confirmed = self.confirm_check()            

            print('do you want to order anything')
            another_order = self.confirm_check()
                
            if another_order:
                # bot ask for another order
                print('please pick another order')
                order_list, state = self.order_response(state, order_list)
                return order_list, state
            else:
                state = 4
                return order_list, state

    def start(self):
        cust_orders = {}
        state = 0 
        intent = ""
        order_list = []
        komplain = []
        info = []
        prev_state = 0
        intent_map = { 
            "greet":0,
            "menu":1,
            "pesan":2,
            "komplain":3,
            "confirm":4,
            "reject":5
        }
        intent_map = switch_keys_values(intent_map)
        state_map = {0:'homepage',
                     1:'exit',
                     2:'out-page',
                     3:'order-loop',
                     4:'order-stop',
                     5:'finalization'}
        while state != 1:
            if state == 0:
                pdb.set_trace()
                if True: #prev_state == 0: #first time chat
                    print('Welcome')
                    user_chat = input()
                    state = self._exit_check(state, user_chat)
                    if state == 1:
                        break
                    
                    intent_pred = self.intent_model.predict([user_chat])[0]
                    pdb.set_trace()
                    if intent_pred in [1,2,3]:
                        state = 2
                        intent = intent_map[intent_pred]
            if state == 2:
                print('state 2')
                prev_state = 2
                if intent == 'komplain':
                    komplain, state = self.complain_response()
                    print(state)
                elif intent == 'menu':
                    state = self.menu_response()
                elif intent == 'pesan':
                    state = 3
                else:
                    print('we dont understand, please check the menu')
                    state = self.menu_response()
                pdb.set_trace()
            
            if state == 3:
                print(state)
                order_list, state = self.order_response(state=3)

            if state == 4:
                prev_state = 4
                #chat all the order
                print(order_list)
                #ask for name and table
                print('input your name and table')
                cust_name = input()
                print(cust_name)
                #user input name and table
                print('thank you')
                #thank you, and reconfirm
                state = 1
        cust_orders = {'orders': order_list,
                       'info': cust_name,
                       'komplain': komplain}
        return cust_orders

if __name__ == '__main__':
    chat_bot=chatBotAssistant()
    chat_bot.start()