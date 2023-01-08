import datasets
from setfit import SetFitModel
import argparse

def result_postprocessing(result):
    label_keys = { 
            0:"greet",
            1:"menu",
            2:"pesan",
            3:"komplain",
            4:"confirm",
            5:"reject"
        }
    return label_keys[result[0]]

def get_args():
    # create the argument parser
    parser = argparse.ArgumentParser()

    # add the arguments
    parser.add_argument("-w", "--weight_folder", default="tweet-indo", type=str, help="config file path")
    
    # parse the arguments
    args = parser.parse_args()

    # print the arguments
    return args

if __name__ == '__main__':
    args = get_args()
    print('weight: ', args.weight_folder)
    if args.weight_folder == 'play-review':
        model = SetFitModel.from_pretrained("randypang/indo-review-sentiment-minilm3"
        )
    elif args.weight_folder == 'tweet-indo':
        model = SetFitModel.from_pretrained("randypang/indo-tweet-sentiment-minilm3")
    else:
        print('using custom weight')
        model = SetFitModel.from_pretrained(args.weight_folder)
    
    while True:
        text = input('write a review: ')
        if text == 'exit':
            break
        result = model.predict([text])
        postproc_result = result_postprocessing(result)
        print('text "{}" is: a {} review'.format(text, postproc_result))