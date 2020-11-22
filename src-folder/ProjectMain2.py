# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 22:13:17 2020

@author: shubhrika
"""
## Files needed to be execution of the code 
#PreProcessing 
import PreProcessData.XmlCollection as xc 
import PreProcessData.Processing as proc

#index 
import Index.MyIndexWriter as IndexWriter
import Index.MyIndexReader as IndexReader

#search
import Search.QueryRetreivalModel as QueryRetreivalModel
import Search.ExtractQuery as ExtractQuery

#File locations
import Classes.Path as Path

#Datetime to get timestamps
import datetime

startTime = datetime.datetime.now()
# Results the pointer to the collection to be used
collection=xc.XmlCollection()

#collection.getAbstract()
index = IndexReader.MyIndexReader()
print(index.getDocumentCount())
query_model=QueryRetreivalModel.QueryRetrievalModel(index)
extractor = ExtractQuery.ExtractQuery()
queries= extractor.getQuries()
for query in queries:
#    results = query_model.retrieveQuery(query, 20)
    print(query)
#query_model.retrieveQuery(queries, 20)
#    id=index.getDocId(file)
#    print(index.getDocLength(id))
#    break
    


endTime = datetime.datetime.now()
print ("Subject Collection time: ", endTime - startTime)

