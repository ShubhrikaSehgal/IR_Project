# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 01:21:23 2020

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

#File locations
import Classes.Path as Path

#Datetime to get timestamps
import datetime

startTime = datetime.datetime.now()
# Results the pointer to the collection to be used
collection=xc.XmlCollection()

abstract_Coll=collection.getAbstract()
processing=proc.Processing()

number=105
doc = []
wr = open(Path.Result + ".xml", "w", encoding="utf8")
for abstract in abstract_Coll:
#    processedAbstract=processing.processContent(abstract)
#    wr.write(str(processedAbstract)+"\n")
    print(abstract)
wr.close()

    
#indexwriter=IndexWriter.MyIndexWriter() 
#indexwriter.index(u'number',processedAbstract)
#    number+=1
#indexwriter.close()

#index = IndexReader.MyIndexReader()
#print(index.getDocumentCount())


## Retrieves all the subjects in the collection 
#subject_collection=collection.getSubjects()
#
## Retrives all the section in the collection 
#
#processing=proc.Processing()
#for subject in subject_collection:
#    processedSubject=processing.processContent(subject)
#    print(processedSubject)



endTime = datetime.datetime.now()
print ("Subject Collection time: ", endTime - startTime)
