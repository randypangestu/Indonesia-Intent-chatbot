import datasets
from setfit import SetFitModel
import argparse

def result_postprocessing(result_proba):
    label_keys = {'1':'POSITIVE',
                  '0':'NEGATIVE',
                  '2':'NEUTRAL'}
    negative_value = result_proba[0,0]
    positive_value = result_proba[0,1]
    if abs(negative_value - positive_value) < 0.2:
        class_predict = 2
    else:
        class_predict = result_proba.argmax()
    print('neg value', negative_value, 'positive value', positive_value)
    return label_keys[str(class_predict)]

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
        model = SetFitModel.from_pretrained(args.weight_folder)
    
    while True:
        text = input('write a review: ')
        if text == 'exit':
            break
        result = model.predict_proba([text])
        postproc_result = result_postprocessing(result)
        print('text "{}" is: a {} review'.format(text, postproc_result))