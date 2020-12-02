# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 07:23:55 2020

@author: 16303
"""
import Classes.Path as Path
import glob
import re 
class DataCreater:
    def __init__(self):
        self.XmlFileLocation=sorted(glob.glob(Path.XmlFileFolder+ '/*.XML'))
        count=0
        wr = open(Path.ResultData + ".txt", "w", encoding="utf8")
        for file in self.XmlFileLocation:
            title,subject,data=self.getData(file)
            wr.write(file+":"+title+":"+subject+":"+data+"\n")
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
        count=0
        while(current_line):
           if(re.search(r'<KeyWords>',current_line)):
                current_line=XmlFile.readline()
                readDoc=True
                subject=True
           elif(re.search(r'</KeyWords>',current_line)):
                readDoc=False
                subject=False
           elif(re.search(r'<Title>',current_line)):
               title=re.compile(r'<[^>]+>').sub('', current_line.strip())
           elif(re.search(r'<Abstract>',current_line)):
                current_line=XmlFile.readline()
                readDoc=True
           elif(re.search(r'</Abstract>',current_line)):
                readDoc=False
                title_string = ''
                for t in title:
                    title_string += t + ' '
                return title," ".join(subjects)," ".join(abstract)
           if(readDoc and subject):
                if(not re.match(r'\n',current_line)):
                    subject_data=re.sub(r'<KeyWord id=.+?>','',current_line).replace("</KeyWord>","").replace("\n","").strip()
                    subjects.add(subject_data)
           elif(readDoc):
               if  current_line.strip():
                   count+=1
                   value=re.compile(r'<[^>]+>').sub('', current_line)
                   abstract_value=re.sub(r'(\&lt\;[^\&]+\&gt\;)([^\&]+|)(\&lt\;[^\&gt\;]+\&gt\;)|(\&lt\;[^\&]+\&gt\;)','',value)
                   abstract_value=re.sub(r'\$\$[^\$]+\$\$','',abstract_value).replace("\n","").strip()
                   #.replace('nbsp;','').replace("\n","").replace("&amp;","").strip()
                   abstract.append(abstract_value)
                   if(count%50==0):
                       return title," ".join(subjects)," ".join(abstract)
           current_line=XmlFile.readline()
        return title," ".join(subjects)," ".join(abstract)