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
#collection=xc.XmlCollection()
read = open(Path.Result + ".txt", "r", encoding="utf8")
write=open(Path.ProcessedResult+".txt","w",encoding="utf8")
processing=proc.Processing()
count=0
while( True):
    docNo=read.readline()
    if( docNo is None or docNo==" "):
        break;
    subject=read.readline()
    content=read.readline()
    count+=1
    write.write(docNo+str(processing.processContent(subject))+"\n"+
               str( processing.processContent(content))+"\n")
    if(count%5000==0):
        print(count)
    if(count%52745==0):
        print(docNo)
        break
write.close()
read.close()
##collection.getAbstract()
#index = IndexReader.MyIndexReader()
## print("Number of documents in collection:", index.getDocumentCount())
#query_model=QueryRetreivalModel.QueryRetrievalModel(index)
#extractor = ExtractQuery.ExtractQuery()
#queries= extractor.getQuries()
#print(queries.get)
#results = query_model.retrieveQuery(queries, 20)[0]
#for doc in results:
#    print(doc.getDocNo(), doc.getScore())

#query_model.retrieveQuery(queries, 20)
#    id=index.getDocId(file)
#    print(index.getDocLength(id))
#    break
    


endTime = datetime.datetime.now()
print ("Subject Collection time: ", endTime - startTime)

