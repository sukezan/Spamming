# coding: utf-8
'''
This program uses training data and discriminant data to determine whether the discriminant data is junk or other mail.
'''
import sys
import csv
import json
import scipy.stats
from collections import Counter
from argparse import ArgumentParser

def import_from_command_line():
    files_path_or_num = sys.argv
    return files_path_or_num

def file_input(file_path,file_path_pd):
    labels = []
    predict_data = {}
    mail_wakati_dict = {}
    file_names = []
    with open(file_path,'r',encoding='utf-8') as f: 
        file_json = json.load(f) 
        mail_wakati_dict = json.loads(file_json) 

    with open(file_path_pd,'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            predict_data = row

    return mail_wakati_dict, predict_data

#Function to calculate the probability of word occurrence from training data
def get_info(mail_wakati_dict):
    word_count = mail_wakati_dict['WORD_COUNT']
    mail_count = mail_wakati_dict['MAIL_COUNT']

    mail_wakati_dict.pop('WORD_COUNT')
    mail_wakati_dict.pop('MAIL_COUNT')

    dict_key = mail_wakati_dict.keys()
    labels = list(dict_key) 
 
    return mail_wakati_dict, word_count, mail_count, labels

#Function to determine the email is spam or something else
def predict(mail_wakati_dict, word_count, mail_count, predict_data, labels, prob_unknown_words):
    probs_dict = {}
    probs_list = []
    max_score = 0
    for label in labels: 
        prob = mail_count[label]/mail_count['ALL'] 
        
        
        for word in predict_data:
            if word not in mail_wakati_dict[label]:
                probs_list.append(prob_unknown_words) #Dealing with unknown words
                continue
            else:
                probs_list.append(mail_wakati_dict[label][word] / word_count[label])
        normalization = [1-n for n in probs_list]
        probs_list.clear() 
        list(normalization)
        
        for num in normalization:
            prob *= num
        normalization.clear()
        probs_dict[label] = prob 
    
    max_label = min(probs_dict, key=probs_dict.get) 
    print(probs_dict)
    print('The label of this mail is '+max_label)

def get_option():
    argparser = ArgumentParser(prog='spam_mail_filter.py', 
                               usage='Determine whether a mail is spam or non-spam.',
                               description='description',
                               epilog='end', 
                               add_help=True, 
                                )

    argparser.add_argument('-td', '--trainedData', type=str,
                           default='trainData.json', 
                           help='Specify the input trained data')

    argparser.add_argument('-dh', '--distinguished', type=str,
                           default='tokenized_data.csv',
                           help='Specify the data to be distinguished')

    argparser.add_argument('-uf', '--unknownFigures', type=float,
                           default=0.01,
                           help='Specify the figures of unknown word')
  
    return argparser.parse_args()

def main():
    args = get_option()
    file_path = str(args.trainedData)
    file_path_pd = str(args.distinguished)
    prob_unknown_words = float(args.unknownFigures)
    mail_wakati_dict, predict_data = file_input(file_path,file_path_pd)
    mail_wakati_dict, word_count, mail_count, labels = get_info(mail_wakati_dict)
    predict(mail_wakati_dict,word_count, mail_count, predict_data,labels,prob_unknown_words)


if __name__ == "__main__":
    main()