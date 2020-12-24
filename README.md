# Spamming
Detect junk or anything else.

## Description 
These tools are programs that tokenize and identify junk mail.(Japanese text only)

## Features
- Tokenize or train tokenized data.
```
$ python3 tokenizer_train.py -h
usage: Tokenize the data or train from the tokenized data.

description

optional arguments:
  -h, --help            show this help message and exit
  -a {train,tokenize}, --algorithm {train,tokenize}
                        Specify the Algorithm
  -ip INPUT, --input INPUT
                        Specify the input file name or path
  -op OUTPUT, --output OUTPUT
                        Specify the output file name or path.(for train: .json, for tokenize: .csv)

```
- Identify email labels from learned data.
```
$ python3 junk_mail_filter.py -h
usage: Determine whether a mail is spam or anything else.

description

optional arguments:
  -h, --help            show this help message and exit
  -td TRAINEDDATA, --trainedData TRAINEDDATA
                        Specify the input trained data
  -dh DISTINGUISHED, --distinguished DISTINGUISHED
                        Specify the data to be distinguished
  -uf UNKNOWNFIGURES, --unknownFigures UNKNOWNFIGURES
                        Specify the figures of unknown word

```

## Requirement
Python3 or more

## Installation
```
git clone https://github.com/sukezan/Spamming.git
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
- Training data must habe label first.
```
// example data (training.txt):
N, 今回の学会発表は2020年3月22日15時より行います。
S, 今週のセール情報：最新の洗濯機がメール会員様限定価格で59800円！
```

## License
sukezan/Spamming is licensed under the MIT License

Copyright (c) 2020 Kosuke Yamagami