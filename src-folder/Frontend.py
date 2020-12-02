# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 13:00:44 2020

@author: shubhrika 
"""
from flask import Flask
from flask import render_template
from flask import request, redirect
import Search.ExtractQuery as ExtractQuery
import Index.MyIndexReader2 as IndexReader
from collections import defaultdict
import FileReader
#search
import Search.QueryRetreivalModel as QueryRetreivalModel
#Datetime to get timestamps
import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom

index = IndexReader.MyIndexReader("xml")
query_model=QueryRetreivalModel.QueryRetrievalModel(index)
extractor = ExtractQuery.ExtractQuery()
i=FileReader.FileReader()
docList={}
app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        startTime = datetime.datetime.now()
        result_names={}
        searchvalue =request.form.get("Search")
        query_result=extractor.preProcessquery(searchvalue)
        results = query_model.retrieveQuery(query_result, 5)[0]
        global docList
        docList=results
        for doc in results:
#            result_names[doc.getDocNo().replace("Springer.tar//Springer//Springer\\",'')]=doc.getSubject()
#            result_names[doc.getDocNo().replace("Springer.tar//Springer//Springer\\",'')]=doc.getScore()
            docNo=doc.getDocNo()
            result_names[doc.getDocId()]=i.content[docNo.replace("\"","")]
            if(len(doc.getSubject())<2):
                if(doc.getSubject()[0]==""):
                    result_names[doc.getDocId()][1]=searchvalue
            
#            print(i.content[docNo])
#            print(doc.getDocNo().replace("Springer.tar//Springer//Springer\\",''), doc.getScore())
        endTime = datetime.datetime.now()    
        print ("Subject Collection time: ", endTime - startTime)
#        query_model=QueryRetreivalModel.QueryRetrievalModel(index)
#        query_retrival=query_model.retrieveQuery(query_result, 20)
        return render_template('check.html',output=result_names,Query=searchvalue,length=len(results))
    
    return render_template('index.html')

@app.route('/page/<docId>', methods=["GET", "POST"])
def load_content(docId):
     print(docId)
    
     global docList
     for doc in docList:
         if(doc.getDocId()==int(docId)):
              file=open(str(doc.getDocNo()),"r",encoding="utf8")
              dom = xml.dom.minidom.parse(file) # or xml.dom.minidom.parseString(xml_string)
              pretty_xml_as_string = dom.toprettyxml()
              print(pretty_xml_as_string)
              return render_template('loadContent.html',xml= pretty_xml_as_string)
#              bs = BeautifulSoup(file, 'xml')
#              print (bs.prettify())
#              xml = ET.fromstring(file)
#              etree.tostring(x, pretty_print=True)
     return render_template('index.html')

# 1) user feedback - 
# 2) subject tagging (statistics)
    # subject based indexing
    # if user queries and the doc shows up but is missing the subject tag -> we tag it
    
# Title
# Subject tags ['3d-printing']  ['how to do 3-d printing']
# docNo:subjects:processed subject\n

if __name__ == '__main__':
   app.run()