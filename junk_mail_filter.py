# coding: utf-8
'''
このプログラムは学習データと判別データより判別データがスパムかそれ以外のメールかを判別する
入力の形：spma_mail_filter.py 学習したデータ.json 判別したいデータ.csv (ファイルの順番、個数は任意) 未知語のスコア
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
        file_json = json.load(f) #jsonファイルを読み込み
        mail_wakati_dict = json.loads(file_json) #jsonファイルを辞書型に変換

    with open(file_path_pd,'r',encoding='utf-8') as f:
        reader = csv.reader(f) #fの内容をcsv.readerはリスト型としてreaderに格納
        for row in reader:
            predict_data = row

    return mail_wakati_dict, predict_data
#mail_wakati = [[],[]]の多重配列でラベルと同じ順番に格納
#labels=['S','N','...']などのラベル格納

#学習データから単語の出現確率を求める関数
def get_info(mail_wakati_dict):
    word_count = mail_wakati_dict['WORD_COUNT']
    mail_count = mail_wakati_dict['MAIL_COUNT']

    mail_wakati_dict.pop('WORD_COUNT')
    mail_wakati_dict.pop('MAIL_COUNT')

    dict_key = mail_wakati_dict.keys() #mail_wakati_dictに含まれる全てのkeyを取得
    labels = list(dict_key) 
 
    return mail_wakati_dict, word_count, mail_count, labels
    #words_Num_dictはラベルごとの全単語数 ex. {N:3902,S:2982,All:6884}

#判別する関数
def predict(mail_wakati_dict, word_count, mail_count, predict_data, labels, prob_unknown_words):
    probs_dict = {}
    probs_list = []
    max_score = 0
    for label in labels: #labelの出現頻度 
        prob = mail_count[label]/mail_count['ALL'] #label毎の全単語数/全単語数
        
        
        for word in predict_data:
            if word not in mail_wakati_dict[label]:
                probs_list.append(prob_unknown_words) #未知語の処理
                continue
            else:
                #print(mail_wakati_dict[label][word])
                probs_list.append(mail_wakati_dict[label][word] / word_count[label])
                #print(word)
                #probにlabel集合内でのwordの頻度/label集合内の全ての単語数j
        normalization = [1-n for n in probs_list]#正規化
        probs_list.clear() 
        list(normalization)
        
        for num in normalization:
            prob *= num
        normalization.clear()
        probs_dict[label] = prob #key、確率がvalueな値を格納した辞書型
    
    max_label = min(probs_dict, key=probs_dict.get) #確率が低い方のkeyを出す
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