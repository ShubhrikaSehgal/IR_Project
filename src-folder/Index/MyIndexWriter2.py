import sys
sys.path.append("../")
import os
from collections import OrderedDict
import heapq
import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
class MyIndexWriter:

    def __init__(self, type):
        self.type = type

        # {word: {docID: term_count, }, }
        self.Index = {} 
        self.word_heap = []
        
        # track doc count and max
        self.count = 0
        self.max = 100000
        self.first = True

        # location in this dictionary is the index ID of this docNo
        #   [[docNo,doclength], 
        #    [docNo,doclength],
        #   ]
        # index -> docNo: readline(index)
        # docNo -> index: linear search for docNo
            # can parse into memory as ordered dict for constant look up
        self.dictionary_docno_to_index = []
        return

    # This method build index for each document.
	# NT: in your implementation of the index, you should transform your string docno into non-negative integer docids,
    # and in MyIndexReader, you should be able to request the integer docid for each docno.
    def index(self, docNo, subject, content):
        # content = content.split(' ')
        self.dictionary_docno_to_index.append(docNo + ',{},{}\n'.format(len(content),subject))
#        print(self.dictionary_docno_to_index)
        ID = len(self.dictionary_docno_to_index)-1
        for i in range(len(content)):
            word = content[i]
            if word in self.Index:
                if ID in self.Index[word]:
                    self.Index[word][ID] += 1
                # add posting ID and word count initialize
                else:
                    self.Index[word][ID] = 1
            # need entire structure
            else:
                self.Index[word] = OrderedDict()
                self.Index[word][ID] = 1
                heapq.heappush(self.word_heap, word)
        self.count+=1
        if self.count == self.max:
            if self.first:
                self.dump_buffer()
                self.first = False
            else:
                self.merge_index()
            self.count = 0
        return

    # first time running, type = self.type to make a main
    def dump_buffer(self, empty=True):
        # use word_heap to empty index
        buffer_path = 'data//index.{}'.format(self.type)
        # buffer_path = '..//' + buffer_path                          # REMOVE UNLESS BEING RUN ALONE
        dict_term_path = 'data//dict_term.{}'.format(self.type)
        # dict_term_path = '..//' + dict_term_path                    # REMOVE UNLESS BEING RUN ALONE

        index_file = open(buffer_path, 'w')
        dict_term_file = open(dict_term_path, 'w')

        while self.word_heap:
            word = heapq.heappop(self.word_heap)
            if word: # skip empty words
                # word:docID,wordcount docID,wordcount 
                row = self.make_row(word)
                index_file.write(row + '\n')
                dict_term_file.write(word +'\n') #+ ' {}\n'.format(i))

        index_file.close()
        dict_term_file.close()
        
        if empty:
            self.empty_buffer()
        return

    def make_row(self, word):
        row = word + ':'
        for pair in self.Index[word].items():
            row += str(pair[0]) + ',' + str(pair[1]) + ' '
        row = row.strip() # remove trailing space
        return row

    def empty_buffer(self):
        self.Index = {}
        self.word_heap = []
        return
    
    def dump_docNo_to_index(self, empty=True):
        docno_to_index_path = 'data//docno_ID.{}'.format(self.type)
        # docno_to_index_path = '..//' + docno_to_index_path             # TODO: REMOVE UNLESS BEING RUN ALONE
        
        docno_file = open(docno_to_index_path, 'w')
        docno_file.writelines(self.dictionary_docno_to_index)
        docno_file.close()
        if empty:
            self.dictionary_docno_to_index=[]
        return

    # Close the index writer, and you should output all the buffered content (if any).
    def close(self):
        if self.first:
            self.dump_buffer()
            self.first=False
        else:
            self.merge_index()
        self.dump_docNo_to_index()
        return

    '''
    NOTES FOR THE FUTURE:
    merger: can be index file path or buffer
        'buffer' - directly merge buffer with main index file
        file path - merge an index file into the main index file (order doesn't really matter)
    '''
    def merge_index(self, merger = 'buffer', empty=True): 
        if merger=='buffer':
            os.rename('data//index.{}'.format(self.type), 'data//_index.{}'.format(self.type)) #..//
            
            main = open('data//_index.{}'.format(self.type), 'r', errors='ignore') #..//
            new_index = open('data//index.{}'.format(self.type), 'w') #..//
            dict_terms = open('data//dict_term.{}'.format(self.type), 'w') #..//

            index_item = main.readline().split(':', 1)
            index_word = index_item[0]
            index_postings = index_item[1]
            if self.word_heap:
                buffer_word = heapq.heappop(self.word_heap)
                buffer = True
            else:
                buffer = False

            while buffer:              
                #if index1[word1] is earlier than index2[word2]:
                if index_word < buffer_word:
                    # put index1[word1] first
                    new_index.write(index_word + ':' + index_postings)
                    dict_terms.write(index_word+'\n')

                    # iterate word1
                    index_item = main.readline().split(':', 1)
                    if index_item[0]:
                        index_word = index_item[0]
                        index_postings = index_item[1]
                    else:
                        break
                elif index_word > buffer_word:
                    row = self.make_row(buffer_word)
                    new_index.write(row + '\n')
                    dict_terms.write(buffer_word+'\n')
                    
                    if self.word_heap:
                        buffer_word = heapq.heappop(self.word_heap)
                    else:
                        break
                    
                # if the index1[word1]==index2[word2]
                else:
                    # merge postings - cannot use make_row() because need to merge postins
                    row = index_word + ':' + index_postings.strip() + ' '
                    for pair in self.Index[buffer_word].items():
                        row += str(pair[0]) + ',' + str(pair[1]) + ' '
                    row = row.strip()
                    new_index.write(row + '\n')
                    dict_terms.write(index_word+'\n')

                    # iterate word1
                    index_item = main.readline().split(':', 1)
                    if index_item[0]:
                        index_word = index_item[0]
                        index_postings = index_item[1]
                    else:
                        break
                    if self.word_heap:
                        buffer_word = heapq.heappop(self.word_heap)
                    else:
                        break
            
            # index ran out first
            if not index_item[0]:
                while self.word_heap:
                    row = self.make_row(buffer_word)
                    new_index.write(row + '\n')
                    dict_terms.write(buffer_word+'\n')

                    # iterate word2
                    buffer_word = heapq.heappop(self.word_heap)

            # buffer ran out first
            elif not self.word_heap:
                while index_item[0]:
                    index_word = index_item[0]
                    index_postings = index_item[1]
                    new_index.write(index_word + ':' + index_postings)
                    dict_terms.write(index_word+'\n')

                    # iterate word1
                    index_item = main.readline().split(':', 1)
            else:
                raise Exception('UnforeseenCase')

            main.close()
            new_index.close()
            dict_terms.close()
            os.remove('data//_index.{}'.format(self.type)) # ..//
            if empty:
                self.empty_buffer()
        else:
            raise Exception(NotImplementedError)

    # Notes:
    # def add_buffer_word_to_index(self, buffer_word, index):
    # def merge_docs(main, new_docs):
    # to remove postings make id negative 

'''
UNIT TESTS:

from MyIndexWriter import MyIndexWriter
test = MyIndexWriter('text')
test.index('1', 'now this is some content alphabet')
test.index('2', 'my name is what')
test.index('3', 'dont know why you say goodbye')
test.index('4', 'everybody dance now')
print(test.Index)
print(test.dictionary_docno_to_index)

import heapq
for i in range(len(test.word_heap)):
    heapq.heappop(test.word_heap)


from PreProcessedCorpusReader import PreprocessedCorpusReader
from MyIndexWriter import MyIndexWriter
test = MyIndexWriter('text')
R = PreprocessedCorpusReader('trecweb')
test.index(*R.nextDocument())
test.index(*R.nextDocument())
test.index(*R.nextDocument())
test.dump_buffer(type='index', empty=False)

file = open('..//data//dict_term.index','r')
file.readline(0)
list=file.readlines(-1)

File = open('..//data//index.text','r')
File.readlines()
for i in range(459):
    File.readline()


'''