'''
Tokenize or train the file input
'''
import os
import json
import csv
import MeCab
from collections import Counter
from argparse import ArgumentParser

mecab = MeCab.Tagger("-Owakati")

def file_input(file_path): 
    sentences = []
    with open(file_path,'r') as f:
        for line in f:
            line = line.rstrip()
            sentences.append(line) 

    return sentences

def switch(algorithm,sentences,output_file):
    if 'train' in algorithm:
        tokenized = mecab_parse(sentences)
        labels, mail_count = labels_get(tokenized)
        labels_dict = classify(tokenized,labels,mail_count)
        word_labels_dict = train(labels_dict,labels)
        make_json_file(labels_dict, output_file)
        print('json file generated')
    elif 'tokenize' in algorithm:
        tokenized = mecab_parse(sentences)
        make_csv(tokenized,output_file)
        print('csv file generated')
# tokenizer
def mecab_parse(sentences):
    tokenized = []
    for line in sentences:
        words_sep = mecab.parse(line).split() 
        tokenized.append(words_sep) 

    return tokenized

def labels_get(tokenized):
    labels_all = []
    mail_count = {}
    for line in tokenized:
        labels_all.append(line[0])
        labels = list(set(labels_all))
    for label in labels:
        mail_count[label] = labels_all.count(label)
    mail_count['ALL'] = len(labels_all)

    return labels, mail_count
        

def classify(tokenized,labels,mail_count):
    labels_dict = {}
    for words_list in tokenized:
        for label in labels:
            if label in words_list: 
                words_list.remove(label)
                if label in labels_dict: 
                    words_list_from_dict = labels_dict[label] 
                    words_list_from_dict += words_list
        
                    labels_dict[label] = words_list_from_dict 
                else:
                    labels_dict[label] = words_list 
    labels_dict['MAIL_COUNT'] = mail_count
    
    return labels_dict

def train(labels_dict,labels):
    word_count = {}
    for label in labels: 
        words_list = labels_dict[label] 
        counter = len(words_list) 
        word_count[label] = counter 

        counted = dict(Counter(words_list)) 
        labels_dict[label] = counted 
    labels_dict['WORD_COUNT'] = word_count

    return labels_dict
    
cwd_path = os.getcwd()

def make_json_file(labels_dict, output_file):
    cwd_json_file = cwd_path + '/' + output_file
    words_with_label_json = json.dumps(labels_dict,ensure_ascii=False)
    with open(cwd_json_file, 'w') as f:
        json.dump(words_with_label_json, f, ensure_ascii=False, indent=4)

def make_csv(tokenized, output_file):
    cwd_file_path = cwd_path + '/' +output_file 
    
    with open(cwd_file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(tokenized)

def get_option():
    argparser = ArgumentParser(prog='tokenizer_train.py', 
                               description='Tokenize the data or train from the tokenized data',
                               epilog='end', 
                               add_help=True, )

    argparser.add_argument('-a', '--algorithm',
                        choices=[ 'train', 'tokenize'],
                        default='train',
                        help='Specify the Algorithm')

    argparser.add_argument('-ip', '--input', type=str,
                           default='training.txt', 
                           help='Specify the input file name or path')

    argparser.add_argument('-op', '--output', type=str,
                           default='trainData.json',
                           help='Specify the output file name or path.(for train: .json, for tokenize: .csv)')
  
    return argparser.parse_args()


def main():
    args = get_option()
    file_path = args.input
    algorithm = args.algorithm
    sentences = file_input(file_path)
    output_file = args.output
    switch(algorithm,sentences,output_file)

if __name__ == '__main__':
    main()
