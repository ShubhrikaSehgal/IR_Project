# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 13:00:44 2020

@author: shubhrika 
"""
from flask import Flask
from flask import render_template
from flask import request, redirect
import Search.ExtractQuery as ExtractQuery
import Index.MyIndexReader as IndexReader
from collections import defaultdict
#search
import Search.QueryRetreivalModel as QueryRetreivalModel

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        searchvalue =request.form.get("Search")
        extractor = ExtractQuery.ExtractQuery()
        query_result=extractor.preProcessquery(searchvalue)
        index = IndexReader.MyIndexReader()
        query_model=QueryRetreivalModel.QueryRetrievalModel(index)
        results = query_model.retrieveQuery(query_result, 20)[0]
        result_names={}
        for doc in results:
            result_names[doc.getDocNo().replace("Springer.tar//Springer//Springer\\",'')]=doc.getSubject()
#            print(doc.getDocNo().replace("Springer.tar//Springer//Springer\\",''), doc.getScore())
            
            
#        query_model=QueryRetreivalModel.QueryRetrievalModel(index)
#        query_retrival=query_model.retrieveQuery(query_result, 20)
            
        return render_template('check.html',output=result_names,Query=searchvalue)
    return render_template('index.html')

if __name__ == '__main__':
   app.run()