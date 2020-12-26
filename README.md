# Spamming
Determine whether a mail is junk or anything else

## Description 
These tools are programs that tokenize and determine whether a mail is junk or anything else.(Japanese text only)

I have not yet confirmed that the English text works. I'm planning to implement that function

## Features
- Tokenize or train tokenized data
```
$ python3 tokenizer_train.py -h
usage: tokenizer_train.py [-h] [-a {train,tokenize}] [-ip INPUT] [-op OUTPUT]

Tokenize the data or train from the tokenized data

optional arguments:
  -h, --help            show this help message and exit
  -a {train,tokenize}, --algorithm {train,tokenize}
                        Specify the Algorithm
  -ip INPUT, --input INPUT
                        Specify the input file name or path
  -op OUTPUT, --output OUTPUT
                        Specify the output file name or path.(for train: .json, for tokenize: .csv)
```
- Identify email labels from learned data
```
$ python3 junk_mail_filter.py -h
usage: spam_mail_filter.py [-h] [-td TRAINEDDATA] [-dh DISTINGUISHED] [-uf UNKNOWNFIGURES]

Determine whether a mail is junk or anything else

optional arguments:
  -h, --help            show this help message and exit
  -td TRAINEDDATA, --trainedData TRAINEDDATA
                        Specify the input trained data
  -dh DISTINGUISHED, --distinguished DISTINGUISHED
                        Specify the data to be distinguished
  -uf UNKNOWNFIGURES, --unknownFigures UNKNOWNFIGURES
                        Specify the figures of unknown word
```

## Demo
<img width="1068" alt="demo-image" src="https://user-images.githubusercontent.com/43489292/103074073-318fed80-460c-11eb-9642-6d17bdcb4a8a.png">

## Requirement
Python3 or more

## Installation
```
$ git clone https://github.com/sukezan/Spamming.git
$ cd Spamming
```

## Usage
1. To generate json file for train data `tokenizer_train.py`:
```
$ python3 tokenizer_train.py -a train -ip training.txt -op trainData.json
```
2. Tokenize the csv data for discrimination is following:
```
$ python3 tokenizer_train.py -a tokenize -ip disc_data.txt -op tokenized_data.csv
```
3. After that you just input the train and tokenized data to `junk_mail_filter.py` :

4. Specify the input data
```
python3 junk_mail_filter.py -td trainData.json -dh tokenized_data.csv -uf 0.001
```

### note:
- Training data must habe label first
```
//example data (training.txt)
// 'N' is label of Non-Spam, 'S' is label of Spam 
N, 今回の学会発表は2020年3月22日15時より行います。
S, 今週のセール情報：最新の洗濯機がメール会員様限定価格で59800円！
```
- Prepare the training data by yourself

## License
sukezan/Spamming is licensed under the MIT License

Copyright (c) 2020 Kosuke Yamagami
