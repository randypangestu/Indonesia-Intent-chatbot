from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import gradio as gr


def predict(input, history=[]):
    # tokenize the new input sentence
    #new_user_input_ids = tokenizer.encode(input + tokenizer.eos_token, return_tensors='pt')
    
    # append the new user input tokens to the chat history
    #bot_input_ids = torch.cat([torch.LongTensor(history), new_user_input_ids], dim=-1)

    # generate a response 
    #history = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id).tolist()

    # convert the tokens to text, and then split the responses into lines
    
    response=[(input,"testt")]
    return response, history

if __name__=='__main__':
    with gr.Blocks() as demo:

        state = gr.Variable(default_value=[('',"Welcome")])
        chatbot = gr.Chatbot(label="Chatbot")
        text = gr.Textbox(label="Your sentence here... (press enter to submit)", default_value="Hi")
        text.submit(predict, [text, state], [chatbot, state])
        text.submit(lambda x: "", text, text)
    
    demo.launch()
    