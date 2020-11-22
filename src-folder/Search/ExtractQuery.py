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
         path_dir= Path.TopicDir
         self.topic_file = open(path_dir,"r",encoding="utf8")
         self.tokenizer = RegexpTokenizer(r'\w+')
         self.sws_english = set(line.strip() for line in open(Path.StopwordDir, "r", encoding="utf8"))
         self.ps=SnowballStemmer("english")
         self.query_list=self.getQueryList()
         
         return
     
    def getQueryList(self):
        current_line=self.topic_file.readline()
        query_list=[]
        if(not current_line):
             self.topic_file.close()
             return None
        while(current_line):
             query_values=Query.Query()
             query_values.setTopicId("1")
             query_values.setQueryContent(self.preProcessquery(current_line))
             query_list.append(query_values)
             current_line=self.topic_file.readline()
        return query_list
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
