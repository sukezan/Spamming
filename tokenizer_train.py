'''
このプログラムはコマンドラインファイルのパスを入力するとそのファイルを分かち書きして出力.
入力の形：import_and_mecab.py 学習データ.txt（任意の数）任意のファイル名.json
'''
import os
import json
import csv
import MeCab
from collections import Counter
from argparse import ArgumentParser

mecab = MeCab.Tagger("-Owakati")

def file_input(file_path): 
    lines = []
    with open(file_path,'r') as f:
        for line in f:
            line = line.rstrip()
            lines.append(line) 

    return lines

def switch(algorithm,lines,output_file):
    if 'train' in algorithm:
        tokenized = mecab_parse(lines)
        labels, mail_count = labels_get(tokenized)
        words_labels_dict = classify(tokenized,labels,mail_count)
        word_labels_dict = train(words_labels_dict,labels)
        make_json_file(words_labels_dict, args.output)
    elif 'tokenize' in algorithm:
        tokenized = mecab_parse(lines)
        make_csv(tokenized,output_file)
# tokenizer
def mecab_parse(lines):
    tokenized = []
    freq_words_with_label = {}
    for line in lines:
        words_sep = mecab.parse(line).split() #分かち書きしたものをwords_sepに格納
        tokenized.append(words_sep) #二重リストに格納 ex. = [['S','値段','は',...],['N','学会','の',...]]

    return tokenized

def labels_get(tokenized):
    labels_all = []
    mail_count = {}
    for line in tokenized:
        labels_all.append(line[0])
        labels = list(set(labels_all))
    for label in labels:
        mail_count[label] = labels_all.count(label)
    mail_count['ALL'] = len(label_all)

    return labels, mail_count
        

def classify(tokenized,labels,mail_count):
    words_list_collect = []
    words_labels_dict = {}
    for words_list in tokenized: #二重ループになってるそれぞれのメールのリスtを取り出
        for label in labels:
            if label in words_list: #もしwords_listにlabelが入っていれば...
                words_list.remove(label)
                if label in words_labels_dict: #words_with_label_dictのkeyにlabelが格納されていれば
                    words_list_from_dict = words_labels_dict[label] 
                    words_list_from_dict += words_list
        
                    words_labels_dict[label] = words_list_from_dict 
                else:
                    words_labels_dict[label] = words_list #ラベルごとの辞書型で格納
    words_labels_dict['MAIL_COUNT'] = mail_count
    
    return words_labels_dict

def train(words_labels_dict,labels):
    word_count = {}
    for label in labels: 
        words_list = words_labels_dict[label] #key=labelのvalue(単語のリスト)を取り出す
        word_Sum_per_label = len(words_list) #words_list内の全単語数(label毎)をword_Sumに格納 

        word_count[label] = word_Sum_per_label #words_Num_dictsに{label:全単語数}を格納

        counted = dict(Counter(words_list)) #単語と頻度の辞書 ex. counted = {"学会":23,"参加":14}
        words_labels_dict[label] = counted #key=labelの辞書にcounted辞書を格納した多重辞書
        #words_trained_dictはラベルごとの単語と頻度を二重辞書型で格納 ex {N:{"学会":32}S:{"値段":12}}
    words_labels_dict['WORD_COUNT'] = word_count

    return words_labels_dict
    
cwd_path = os.getcwd()

def make_json_file(words_labels_dict, output_file):
    cwd_json_file = cwd_path + '/' + output_file
    words_with_label_json = json.dumps(words_labels_dict,ensure_ascii=False)
    with open(cwd_json_file, 'w') as f:
        json.dump(words_with_label_json, f, ensure_ascii=False, indent=4)

def make_csv(words_sep_double_list, output_file):
    cwd_file_path = cwd_path + '/' +output_file 
    
    with open(cwd_file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(words_sep_double_list)

def get_option():
    argparser = ArgumentParser(prog='tokenizer_train.py', 
                               usage='Tokenize the data or train from the tokenized data.',
                               description='description',
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
    lines = file_input(file_path)
    output_file = args.output
    switch(algorithm,lines,output_file)

if __name__ == '__main__':
    main()
