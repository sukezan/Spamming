# Spamming
Detect junk or non-junk mail.

## Description 
These tools are programs that tokenize and identify junk mail.

## Features
- Tokenize or train tokenized data.
- Identify email labels from learned data.

## Requirement
Python3 or more

## Usage
1. Use `python3 tokenizer_train.py -h` to show how to use this program:
```
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

end
```
2. To generate json file for train data is following:
```

$ python3 tokenizer_train.py -a train -ip training.txt -op trainData.json
```
3. Tokenize the csv data for discrimination
```

$ python3 tokenizer_train.py -a tokenize -ip disc_data.txt -op tokenized_data.csv
```

4. After that you just input the train and tokenized data to `junk_mail_filter.py` :