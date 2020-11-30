# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 08:54:40 2020

@author: 16303
"""
#File locations
import Classes.Path as Path
import PreProcessData.XmlCollection as xc 
import Index.MyIndexWriter2 as IndexWriter
#Datetime to get timestamps
import datetime

startTime = datetime.datetime.now()
processedresult=open(Path.ProcessedResult+".txt","r",encoding="utf8")
indexwriter=IndexWriter.MyIndexWriter("xml") 
collection=xc.XmlCollection()
count=0
docNo=processedresult.readline()
while(docNo):
    processedSubject=processedresult.readline()
    processedData=processedresult.readline()
    indexwriter.index(docNo," ".join(processedSubject),processedData)
    docNo=processedresult.readline()
    
indexwriter.close()
endTime = datetime.datetime.now()
print ("Subject Collection time: ", endTime - startTime)