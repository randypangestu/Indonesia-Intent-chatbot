from setfit import SetFitModel
import pdb
import gradio as gr

pdb.set_trace = lambda: 1
state_map = {0:'homepage',
                     1:'exit',
                     2:'out-page',
                     3:'order-loop',
                     4:'order-stop',
                     5:'finalization'}


def switch_keys_values(dictionary):
    return {value: key for key, value in dictionary.items()}

class chatBotAssistant():
    def __init__(self):
        self._load_intent_model('intent_model') 
        intent_map = { 
            "greet":0,
            "menu":1,
            "pesan":2,
            "komplain":3,
            "confirm":4,
            "reject":5
        }
        self.intent_map = switch_keys_values(intent_map)

        self.
    
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

    def start(self, state,):
        cust_orders = {}
        state = 0 
        order_list = []
        komplain = []
        self.intent_map = { 
            "greet":0,
            "menu":1,
            "pesan":2,
            "komplain":3,
            "confirm":4,
            "reject":5
        }
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
        return state, cust_orders

    def responses(self, mode='welcome'):
        if mode == 'welcome':
            response = "Hi!!! Selamat Datang dengan saya tuyul chatbot, apakah anda ingin melihat menu kami, langsung pesan, atau mengajukan komplain?"
        if mode == 'after-komplain':
            response = "Terima kasih atas feedbacknya kakak, apakah anda ingin 'exit', atau melihat menu kami?"
        if mode == 'menu':
            response = "kopi cappucino 10k \n kopi kenangan 10k \n kopi latte 12k \n es teh manis 8k \n temulawak 5k \n air putih 5k \n ayam tiren 20k \n"
        if mode == 'komplain-in':
            response = "Maaf jika Anda merasa tidak puas dengan pelayanan kami. Apa yang bisa saya bantu untuk memperbaiki keadaan?"
        if mode == "pesan-1":
            response = "Apa yang ingin Anda pesan? Kami menawarkan berbagai macam kopi, teh, dan minuman dingin lainnya. Juga tersedia aneka pilihan makanan ringan seperti ayam tiren. Apa yang ingin Anda pesan?"
        if mode == "confirm":
            response = "apakah anda ingin mengkonfirmasi pesana ini? (y/n)"
        if mode == "pesan-2":
            response = "Apakah anda ingin memesan pesanan lain?"
        if mode == "reject-1":
            response = ""
        return response

    def predict(self, input, history=[], infos={'state':[0,0],'orders':[], 'komplain':"", 'profile':""}):
        state = infos['state']
        if state[0] == 0:
            if state[0] == 0:
                response = 
        
        if state == 0:
            
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

        
        responses.append((input, bot_response))
        return responses, history, infos




def predict(input, state=0, infos=[]):
    # tokenize the new input sentence
    if state == 0:
        print('Welcome')
        user_chat = input()
        state = bot._exit_check(state, user_chat)
        if state == 1:
        
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

    new_user_input_ids = tokenizer.encode(input + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([torch.LongTensor(history), new_user_input_ids], dim=-1)

    # generate a response 
    history = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id).tolist()

    # convert the tokens to text, and then split the responses into lines
    response = tokenizer.decode(history[0]).split("<|endoftext|>")
    response = [(response[i], response[i+1]) for i in range(0, len(response)-1, 2)]  # convert to tuples of list
    return response, history, infos

if __name__=='__main__':
    bot = chatBotAssistant()

    with gr.Blocks() as demo:

        state = gr.Variable(default_value=[('hi','welcome to tuyul chatbot')])
        chatbot = gr.Chatbot(label='Tuyul Asistent')
        text = gr.Textbox(label="Your sentence here... (press enter to submit)", default_value="Hi!")
        
        text.submit(bot.predict, [text, state], [chatbot, state])
        text.submit(lambda x: "", text, text)
    
    demo.launch()