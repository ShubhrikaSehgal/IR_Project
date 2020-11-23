# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 02:51:32 2020

@author: shubhrika
"""
#File locations
import Classes.Path as Path
#Tokenizer
from nltk.tokenize import RegexpTokenizer
#Stemmer
from nltk.stem import SnowballStemmer


class Processing:
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.sno = SnowballStemmer('english')
        self.sws_english = set(line.strip() for line in open(Path.StopwordDir, "r", encoding="utf8"))
        return None
    
    def processContent(self,content):
        # Tokenize 
        tokens = self.tokenizer.tokenize(content)
        # Normalization
        stemmedWords = []
        for token in tokens:
            token = token.lower()
            if token not in self.sws_english:
                stemmedWords.append(self.sno.stem(token))
        return stemmedWords

