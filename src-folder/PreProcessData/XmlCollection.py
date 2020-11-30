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
import Index.MyIndexWriter2 as IndexWriter

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
    
    def getAbstract(self):
        ############## Testing 
        
        ##############
        #open files one by one to add abstract

        count=0
#        processing=proc.Processing()
#        indexwriter=IndexWriter.MyIndexWriter("xml") 
        wr = open(Path.Result + ".txt", "w", encoding="utf8")
        for file in self.XmlFileLocation:
            subject,data=self.getData(file)

#            indexwriter.index(file,(" ".join(processedSubject), " ".join(subject)),processedData)
#            ######################## Testing  
            wr.write(file+"\n"+subject+"\n"+data+"\n")
            count+=1
            if(count%5000==0):
                print(count)
            #######################4
#        indexwriter.close()
        wr.close()
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
           elif(re.search(r'<Abstract>',current_line)):
                current_line=XmlFile.readline()
                readDoc=True
           elif(re.search(r'</Abstract>',current_line)):
                readDoc=False
                return str(subjects),str(abstract)
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
        return str(subjects),str(abstract)
        