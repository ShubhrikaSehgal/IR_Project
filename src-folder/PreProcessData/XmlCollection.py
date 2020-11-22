# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 01:27:57 2020

@author: shubhrika
"""
#File locations
import Classes.Path as Path
#PreProcessing 
import PreProcessData.Processing as proc
#index 
import Index.MyIndexWriter as IndexWriter

# glob is used to import multiple file location folder
import glob
# re is for regular Expression
import re 

from collections import defaultdict

class XmlCollection:
    ## open file location of the document collection
    def __init__(self):
        
#        self.trecTextFile=open(Path.XmlFile,"r",encoding="utf8")
        # open file folder 
        self.XmlFileLocation=sorted(glob.glob(Path.XmlFileFolder+ '/*.XML'))
        return
#    ## get content of the document
#    def getSubjects(self):
#        ############## Testing 
#        count=0
#        ##############
#        #open files one by one to add subjects
#        subjects = set()
#        for file in self.XmlFileLocation:
#            count+=1
#            XmlFile=open(file,"r",encoding="utf8")
#            # check if there is any content in the document
#            current_line=XmlFile.readline()
#            if (not current_line):
#                XmlFile.close() 
#                return
#            # read data, line by line if readDoc is True
#            readDoc=False
#            while(current_line):
#                if(re.search(r'<KeyWords>',current_line)):
#                    current_line=XmlFile.readline()
#                    readDoc=True
#                elif(re.search(r'</KeyWords>',current_line)):
#                    readDoc=False
#                if(readDoc):
#                    if(not re.match(r'\n',current_line)):
#                        subjects.add(re.sub(r'<KeyWord id=.+?>','',current_line).replace("</KeyWord>","").replace("\n","").strip())
#                current_line=XmlFile.readline()
#                
#            ######################## Testing        
##            if(count==50):   
##                break
#            if(count%5000==0):
#                print(count)
#            #######################4
#        
#        print(count)
#        return subjects
    
    def getAbstract(self):
        ############## Testing 
        
        ##############
        #open files one by one to add abstract

        count=0
        processing=proc.Processing()
        indexwriter=IndexWriter.MyIndexWriter() 
        for file in self.XmlFileLocation:
            subject,data=self.getData(file)
            processedSubject=processing.processContent(subject)
            processedData=processing.processContent(data)
            indexwriter.index(file,processedSubject,processedData)
            ######################## Testing  
            count+=1
#            if(count==5):   
#                break
            
            if(count%5000==0):
                print(count)
            #######################4
        indexwriter.close()
        return None 
        
        
        
    def getData(self,file):
        subjects = set()
        abstract = []
        XmlFile=open(file,"r",encoding="utf8")
        # check if there is any content in the document
        current_line=XmlFile.readline()
        if (not current_line):
            XmlFile.close() 
            return
        # read data, line by line if readDoc is True
        readDoc=False
        subject=False
        while(current_line):
           if(re.search(r'<KeyWords>',current_line)):
                current_line=XmlFile.readline()
                readDoc=True
                subject=True
           elif(re.search(r'</KeyWords>',current_line)):
                readDoc=False
                subject=False
           elif(re.search(r'<Body>',current_line)):
                current_line=XmlFile.readline()
                readDoc=True
           elif(re.search(r'</Body>',current_line)):
                readDoc=False
           if(readDoc and subject):
                if(not re.match(r'\n',current_line)):
                    subject_data=re.sub(r'<KeyWord id=.+?>','',current_line).replace("</KeyWord>","").replace("\n","").strip()
                    subjects.add(subject_data)
           elif(readDoc):
               value=re.compile(r'<[^>]+>').sub('', current_line)
               abstract_value=re.sub(r'(\&lt\;[^\&]+\&gt\;)([^\&]+|)(\&lt\;[^\&gt\;]+\&gt\;)|(\&lt\;[^\&]+\&gt\;)','',value)
               abstract_value=re.sub(r'\$\$[^\$]+\$\$','',abstract_value).replace("\n","").strip()
               #.replace('nbsp;','').replace("\n","").replace("&amp;","").strip()
               abstract.append(abstract_value)
           current_line=XmlFile.readline()
#           print(str(subjects)+"\n"+str(abstract))
        return str(subjects),str(abstract)
        