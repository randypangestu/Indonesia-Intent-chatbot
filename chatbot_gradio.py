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
        self._load_intent_model('randypang/intent-simple-chat') 
        intent_map = { 
            "greet":0,
            "menu":1,
            "pesan":2,
            "komplain":3,
            "confirm":4,
            "reject":5
        }
        self.intent_map = switch_keys_values(intent_map)
    
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


    def responses(self, mode='welcome'): # this could be a json file or yaml
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
            response = "apakah anda ingin mengkonfirmasi pesanan ini? (y/n)"
        if mode == "pesan-2":
            response = "Apakah anda ingin memesan pesanan lain?"
        if mode == "pesan-3":
            response = "Silahkan ulangi pesanan anda"
        if mode == "reject-table":
            response = "Pesanannya atas nama siapa? table berapa kak?  "
        if mode == "after-table":
            response = "Terima kasih kak atas pesanannya, pesanan kakak adalah [pesanan] /n mohon ditunggu ya :)"
        return response

    def predict(self, input, history=[], infos={'state':[0,0],'orders':[], 'komplain':"", 'profile':""}): # state could be a list of str for better clarity
        state = infos['state']
        if state[0] == 0:
            if state[1] == 0:
                response = self.responses(mode='welcome')
                infos['state'] = [0,1]
                history.append((input, response))
                return history, history , infos
            if state[1] == 1:
                intent_pred = self.intent_model.predict([input])[0]
                state = [1,0]
        if state[0] == 1:
            if state[1] == 0:
                intent = self.intent_map[intent_pred]
                response_map = {'komplain': ['komplain-in', [2,0]],
                                'pesan': ['pesan-1', [4,0]],
                                'menu': ['menu',[4,0]]}
                response = self.responses(response_map[intent][0])
                state = response_map[intent][1]
                infos['state'] = state
                history.append((input, response))
                return history, history, infos
        if state[0] == 2:
            if state[1] == 0:
                response = self.responses(mode='after-komplain')
                state = [0,1]
                infos['state']=state
                infos['komplain'] =input
                history.append((input, response))

                return history, history, infos
        if state[0] == 3:
            if state[1] == 0:
                response = self.responses(mode='menu')
                state = [4,0]
                infos['state'] = state
                history.append((input, response))
                return history, history, infos
        if state[0] == 4:
            if state[1] == 0:
                response = self.responses(mode='confirm')
                response = response + input
                state = [4,1]
                infos['state'] = state
                infos['orders'].append(input)
                history.append((input, response))
                return history, history, infos

            if state[1] == 1:
                intent_pred = self.intent_model.predict([input])[0]
                intent = self.intent_map[intent_pred]
                response_map = {'confirm': ['pesan-2', [4,2]],
                                'reject': ['pesan-3', [4,0]],
                                'menu': ['pesan-3',[4,0]]}
                response = self.responses(response_map[intent][0])
                state = response_map[intent][1]
                if state[1] == 0:
                    infos['order'].pop()
                infos['state'] = state
                history.append((input, response))
                return  history, history, infos
            if state[1] == 2:
                intent_pred = self.intent_model.predict([input])[0]
                intent = self.intent_map[intent_pred]
                response_map = {'confirm': ['pesan-1', [4,0]],
                                'reject': ['reject-table',[5,0]]}
                response = self.responses(response_map[intent][0])
                state = response_map[intent][1]
                infos['state'] = state
                history.append((input, response))
                return history, history, infos
        if state[0] == 5:
            if state[1] == 0:
                response = self.responses(mode='after-table')
                response = response.split('[pesanan]')
                response = response[0] + ','.join(infos['orders']) + response[1]
                state = [5,1]
                infos['state'] = state
                infos['profile'] = input
                history.append((input, response))
                return history, history, infos
            if state[1] == 1:
                exit()
                return history, history, infos



if __name__=='__main__':
    bot = chatBotAssistant()

    with gr.Blocks() as demo:

        state = gr.Variable([])
        state1 = gr.Variable({'state':[0,0],'orders':[], 'komplain':"", 'profile':""})
        chatbot = gr.Chatbot(label='Tuyul Asistent')
        text = gr.Textbox(label="Your sentence here... (press enter to submit)", default_value="Hi!")
        
        text.submit(bot.predict, [text, state, state1], [chatbot, state, state1])
        text.submit(lambda x: "", text, text)
    
    demo.launch()