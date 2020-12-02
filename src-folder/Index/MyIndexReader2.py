import sys
sys.path.append("../")
import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
class MyIndexReader:

    def __init__(self, type):
        self.type = type
        
        # initialize dictionary of terms
        terms_file = open('data//dict_term.{}'.format(self.type), 'r', errors='ignore') #..//
        terms = terms_file.readlines()
        self.term_dict = {}
        for i in range(len(terms)):
            self.term_dict[terms[i].strip()] = i
        terms_file.close()
        terms = None

        docIDs_file = open('data//docno_ID.{}'.format(self.type), 'r', errors='ignore') #..//
        IDs = docIDs_file.readlines()
        self.number_of_docs = len(IDs)
        self.docNo_to_docIDs = {}
        self.docIDs_to_docNo = {}
        self.total_words = 0                   # if want fractional frequency instead of count
        for i in range(len(IDs)):
#            print(IDs[i])
            line = IDs[i].strip().split(',')
            self.docNo_to_docIDs[line[0]] = (i, line[1],line[2:])
            self.docIDs_to_docNo[i] = line[0]
            self.total_words += int(line[1])    # if want fractional frequency instead of count
        docIDs_file.close()
        IDs=None

        self.index = open('data//index.{}'.format(self.type), 'r', errors='ignore') #..//

    # Return the integer DocumentID of input string DocumentNo.
    def getDocId(self, docNo):
        return self.docNo_to_docIDs[docNo][0]
    
    def getDocLength(self,docNo):
        return int(self.docNo_to_docIDs[docNo][1])
    
    def getDocSubject(self, docNo):
        return self.docNo_to_docIDs[docNo][2]

    # Return the string DocumentNo of the input integer DocumentID.
    def getDocNo(self, docId):
        # print(docId, type(docId))
        if type(docId).__name__ == 'dict':
            docId=list(docId.keys())[0]
        return self.docIDs_to_docNo[docId]

    def find_line_index(self, line_no):
        for i, line in enumerate(self.index):
            if i==line_no:
                self.index = open('data//index.{}'.format(self.type), 'r', errors='ignore') # ..//
                return line

    # Return DF.
    def DocFreq(self, token):
        line_no = self.term_dict[token]
        term_postings = self.find_line_index(line_no).split(':')
        postings = term_postings[1].split(' ')
        return len(postings) #/self.number_of_docs

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        line_no = self.term_dict[token]
        line = self.find_line_index(line_no).split(':')
        postings = line[1].split(' ')
        total=0
        for i in range(len(postings)):
            count = postings[i].split(',')[1]
            total += int(count)
        
        return total #/self.total_words

    # Return posting list in form of {documentID:frequency}.
    def getPostingList(self, token):
        line_no = self.term_dict[token]
        line = self.find_line_index(line_no).split(':')
        postings = line[1].split(' ')
        postings_list = {}
        for i in range(len(postings)):
            doc, count = postings[i].split(',')
            postings_list[int(doc)] = int(count)
        return postings_list

'''
Notes:
Can use readline(number) to read specific lines in file

from PreProcessedCorpusReader import PreprocessedCorpusReader
from MyIndexWriter import MyIndexWriter
test = MyIndexWriter('text')
R = PreprocessedCorpusReader('trecweb')
test.index(*R.nextDocument())
test.index(*R.nextDocument())
test.index(*R.nextDocument())
test.index(*R.nextDocument())
test.close()

from MyIndexReader import MyIndexReader
test_r = MyIndexReader('text')
test_r.getDocId('lists-000-0033077')
test_r.getDocNo(3)
test_r.DocFreq('est')
test_r.CollectionFreq('est')
test_r.getPostingList('est')

from MyIndexReader import MyIndexReader
test_r = MyIndexReader('trecweb')
test_r.getDocNo(3)

'''

