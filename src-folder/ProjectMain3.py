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
    processedSubject=processedresult.readline().strip()[1:-1].split(', ')
    processedData=processedresult.readline().strip()
    #'human','machin',
    processedSubject_String = ''
    for sub in range(len(processedSubject)):
        processedSubject_String += processedSubject[sub][1:-1]
        if sub < len(processedSubject)-1:
            processedSubject_String += ','
    indexwriter.index(docNo.strip(),processedSubject_String,processedData.replace("\'","").split(","))
    docNo=processedresult.readline()
    if(count%5000==0):
        print(count)
    count+=1
    
indexwriter.close()
endTime = datetime.datetime.now()
print ("Subject Collection time: ", endTime - startTime)