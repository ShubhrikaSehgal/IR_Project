# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 07:15:11 2020

@author: 16303
"""
#File locations
import Classes.Path as Path
import DataCreater
import datetime
class FileReader:
     def __init__(self):
         values = open(Path.ResultData + ".txt", "r", encoding="utf8", errors='ignore')
         data = values.readlines()
         self.content={}
         startTime = datetime.datetime.now()
         for i in range(len(data)):
             line =data[i].strip().split(':')
             self.content[line[0]] = (line[1],
                         line[2],line[3])
         endTime = datetime.datetime.now()
         print ("Subject Collection time: ", endTime - startTime)
         return None

#     def writer():
#DataCreater.DataCreater()
#
         

    