from datasets import load_dataset
from setfit import sample_dataset
from setfit import SetFitModel, SetFitTrainer, DistillationSetFitTrainer
from sentence_transformers import InputExample, losses


import argparse
import logger
import yaml


def train_teacher(dataset, pretrained="firqaaa/indo-sentence-bert-base"):

    # Load pretrained model from the Hub
    teacher_model = SetFitModel.from_pretrained(pretrained)
    # Create trainer
    print(dataset)
    column_mapping = {"text": "text", "intent": "label"}
    teacher_trainer = SetFitTrainer(
        model=teacher_model, train_dataset=dataset,
        column_mapping = column_mapping,
        num_epochs= 2)
    # Train!
    teacher_trainer.train()
    return teacher_trainer


def train_distill(teacher_model, distill_dataset, student_model='sentence-transformers/paraphrase-MiniLM-L3-v2', model_name='distilled model' ):


    student_model = SetFitModel.from_pretrained(
        student_model
    )
    student_trainer = DistillationSetFitTrainer(
        teacher_model=teacher_model,
        train_dataset=distill_dataset,
        student_model=student_model,
        
    )
    student_trainer.train()

    return student_trainer, pb

def dataset_preparation(dataset_name='jakartaresearch/google-play-review'):
    if dataset_name.endswith('json'):
        dataset = load_dataset("json", data_files=dataset_name, field='data')
    else:
        dataset = load_dataset(dataset_name)
    dataset_split = dataset['train']
    print('split',dataset_split)
    # Create 2 splits: one for few-shot training, the other for knowledge distillation
    train_dataset_few_shot = sample_dataset(dataset_split, num_samples=70, label_column="intent")
    #train_dataset_distill = train_dataset["test"].select(range(1000))
    #test_dataset = dataset["test"]
    print(train_dataset_few_shot.shape)
    dataset_dict = {'few_shot':dataset_split,
                    }
    return dataset_dict


def train_and_distill(dataset_dict, model_config):
    # prepare dataset for training
    train_dataset_few_shot = dataset_dict['few_shot']
    train_dataset_distill = dataset_dict['distill']
    
    
    logger.info('TRAIN TEACHER MODEL')
    teacher_trainer = train_teacher(dataset=train_dataset_few_shot, pretrained=model_config['train_params']['teacher_model'])
    logger.info('Finished training teacher')

    logger.info('TRAIN STUDENT MODEL WITH DISTILLATION')
    student_model_trainer = train_distill(distill_dataset=train_dataset_distill,
                                                      student_model=model_config['train_params']['student_model'])
    logger.info('Finished training student model')
    
    return student_model_trainer 


def read_yaml_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def get_args():
    # create the argument parser
    parser = argparse.ArgumentParser()

    # add the arguments
    parser.add_argument("-c", "--config",  required=True, type=str, help="config file path")
    parser.add_argument("-s", "--save_path", required=True, type=str, help="number of items to process")
    # parse the arguments
    args = parser.parse_args()

    # print the arguments
    return args

if __name__ == '__main__':
    args = get_args()
    config = read_yaml_config(args.config)
    dataset_dict = dataset_preparation(config['train_params']['dataset'])
    train_few_shot = dataset_dict['few_shot']
    teacher_train = train_teacher(dataset=train_few_shot, pretrained=config['train_params']['teacher_model'])
    teacher_train.model._save_pretrained(args.save_path)
   