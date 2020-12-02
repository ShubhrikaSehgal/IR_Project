import Classes.Query as Query
from collections import defaultdict
from Classes.Document import Document
from operator import attrgetter
import heapq


class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader, mu=1980):
        self.indexReader = ixReader
        self.corpus_term_freq=defaultdict(int)
        self.documentLength = defaultdict(int)
        self.termDocumentFreq=defaultdict(dict)
        self.mu=mu
        self.collection_wordCount=self.indexReader.total_words
#        print(self.indexReader.total_words)
#        for i in range(self.indexReader.getDocumentCount()):
#             self.collection_wordCount +=self.indexReader.getDocLength(i) 
        return

    def DirichletProb(self, wCount_D, wProb_C, docLen, mu):
        return (wCount_D + mu*wProb_C) / ((docLen) + mu)

    def retrieveQuery(self, query, topN): #Dirichlet_
        tokens = query

        # Couldn't find a meta data value for whoosh index for this so just built it in... slow to do 4 times
        # if not self.collection_wordCount:
        #     self.getCollectionWordCount()

        # {token: postingsList, }
        postingsLists = {}
        # {documentId: (len(document), {token: prob}), } for all seen documents of all tokens
        docList = {}
        # {token: collectionfrequency}
        tokenFreq_C = {}
        noneInCollection = []
        # build info needed for model
        for token in tokens:
            print(token)
            tokenFreq_C[token] = self.indexReader.CollectionFreq(token)
            print(tokenFreq_C[token])
            if tokenFreq_C[token] == 0:
                noneInCollection.append(token)
            else:
                postingsLists[token] = self.indexReader.getPostingList(token)
                # if the word exists in the index            
                for docId in postingsLists[token].keys():
                    if docId not in docList:
                        docList[docId] = [self.indexReader.getDocLength(self.indexReader.getDocNo(docId)), {}]

        for token in noneInCollection:
            tokens.remove(token)
        # Word not in collection: TA says to ignore word
        # if noneInCollection:
            # print(" *** WARNING! *** ")
            # print("-> The following word(s) not in the collection: ", *noneInCollection)
            # print("Please check if your stemming matches.")
            # print("-> DEFAULT BEHAVIOR: Omit words from query that don't exist in the collection.")
            # only use line below if you want to not return any documents.
            # return []


        # calculate scores and push onto heap
        heap = []
        for docId, docInfo in docList.items():
            docLen = docInfo[0]
            docProb = 1.
            for token in tokens:
                # if token exists in document or not
                if docId in postingsLists[token]:
                    wCount_D = postingsLists[token][docId]
                else:
                    wCount_D = 0
                wProb_C = tokenFreq_C[token]/self.collection_wordCount
                # docLen = handled by loop
                prob = self.DirichletProb(wCount_D, wProb_C, docLen, self.mu)
                docProb *= prob
                docInfo[1][token] = prob
                # docLogProb *= math.log(self.DirichletProb(wCount_D, wProb_C, docLen, self.mu))

            # push (-docProb, docId) onto heap
            # min heap so multiply by -1 to get largest value up top
            heapq.heappush(heap, (docProb*(-1), docId))

        ret = []
        for i in range(topN):
            if len(heap)==0:
                break
            docScore, docId = heapq.heappop(heap)
            doc = Document()
            doc.setDocId(docId)
            doc.setDocNo(self.indexReader.getDocNo(docId))
            doc.setSubject(self.indexReader.getDocSubject(self.indexReader.getDocNo(docId)))
            doc.setScore(docScore*(-1)) # convert back to positive number
            ret.append(doc)

        return ret, tokens, tokenFreq_C, postingsLists, docList
    
    # get number of words in collection, should only do once
    # def getCollectionWordCount(self):
    #     self.collection_wordCount = 0
    #     for doc in self.indexReader.searcher.documents():
    #         self.collection_wordCount += len(doc['doc_content'].split(" "))
    #     return

    def TermCollectionFreq(self, word):
        if word not in self.corpus_term_freq:
            self.corpus_term_freq[word] = self.indexReader.CollectionFreq(word)
        return self.corpus_term_freq[word]
    
        
    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    # def retrieveQuery(self, query, topN):
    #     self.document_result=defaultdict(int)
    #     queries_result=query.getQueryContent()
    #     for word in queries_result:
    #         print(word)
    #         posting_list=self.indexReader.getPostingList(word)
    #         self.indexReader.setTermDocumentFreq(word,posting_list)
    #         for document_id in  posting_list.keys():
    #             self.document_result[document_id]=Document.Document()
    #             self.document_result[document_id].setDocNo(self.indexReader.getDocNo(document_id))
    #             self.document_result[document_id].setScore(self.dirichletSmoothMeth(queries_result,document_id))
    #             self.document_result[document_id].setDocId(document_id)
    #     return [doc for doc in sorted(self.document_result.values(), key=attrgetter('score'), reverse = True)][:topN]
    
    # def dirichletSmoothMeth(self, queries, document_id):
    #     doc_score = 1.0 
    #     document_len = self.indexReader.getDocLength(document_id)
    #     document_len_adj = document_len + self.mu
    #     adj_length=self.mu/self.length
    #     for word in queries:
    #         Collection_freq = self.TermCollectionFreq(word)
    #         if Collection_freq:
    #             docTermFrequency = self.indexReader.getTermDocumentFreq(word, document_id)
    #             doc_score *=  (docTermFrequency + adj_length * Collection_freq)/document_len_adj
    #     return doc_score
    

          