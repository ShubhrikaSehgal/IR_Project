import Classes.Query as Query
import Classes.Path as Path
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer


class ExtractQuery:

    def __init__(self):
        # 1. you should extract the 4 queries from the Path.TopicDir
        # 2. the query content of each topic should be 1) tokenized, 2) to lowercase, 3) remove stop words, 4) stemming
        # 3. you can simply pick up title only for query.
         self.tokenizer = RegexpTokenizer(r'\w+')
         self.sws_english = set(line.strip() for line in open(Path.StopwordDir, "r", encoding="utf8"))
         self.ps=SnowballStemmer("english")
         
         return
     
    def getQueryList(self,value):
         query_values=Query.Query()
         query_values.setTopicId("1")
         query_values.setQueryContent(self.preProcessquery(value))
         return query_values
    def preProcessquery(self,content):
        ## tokenized 
        bag_of_words=self.tokenizer.tokenize(content)
        normalized_words=[]
        for word in bag_of_words:
            ## to lowercase 
            lowercase=word.lower()
            ## remove stop words 
            if lowercase not in self.sws_english:
                ## stemming 
                normalized_words.append(self.ps.stem(lowercase))
        return normalized_words

    # Return extracted queries with class Query in a list.
    def getQuries(self):
        return self.query_list
