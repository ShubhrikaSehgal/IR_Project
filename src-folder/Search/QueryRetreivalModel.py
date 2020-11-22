import Classes.Query as Query
from collections import defaultdict
import Classes.Document as Document
from operator import attrgetter

class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader):
        self.indexReader = ixReader
        self.corpus_term_freq=defaultdict(int)
        self.documentLength = defaultdict(int)
        self.termDocumentFreq=defaultdict(dict)
        self.mu=1980
        self.length=0
        for i in range(self.indexReader.getDocumentCount()):
             self.length +=self.indexReader.getDocLength(i) 
        return


    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    def retrieveQuery(self, query, topN):
        self.document_result=defaultdict(int)
        queries_result=query.getQueryContent()
        for word in queries_result:
            print(word)
            posting_list=self.indexReader.getPostingList(word)
            self.indexReader.setTermDocumentFreq(word,posting_list)
            for document_id in  posting_list.keys():
                self.document_result[document_id]=Document.Document()
                self.document_result[document_id].setDocNo(self.indexReader.getDocNo(document_id))
                self.document_result[document_id].setScore(self.dirichletSmoothMeth(queries_result,document_id))
                self.document_result[document_id].setDocId(document_id)
        return [doc for doc in sorted(self.document_result.values(), key=attrgetter('score'), reverse = True)][:topN]
    
    def dirichletSmoothMeth(self, queries, document_id):
        doc_score = 1.0 
        document_len = self.indexReader.getDocLength(document_id)
        document_len_adj = document_len + self.mu
        adj_length=self.mu/self.length
        for word in queries:
            Collection_freq = self.TermCollectionFreq(word)
            if Collection_freq:
                docTermFrequency = self.indexReader.getTermDocumentFreq(word, document_id)
                doc_score *=  (docTermFrequency + adj_length * Collection_freq)/document_len_adj
        return doc_score
    
    def TermCollectionFreq(self, word):
        if word not in self.corpus_term_freq:
            self.corpus_term_freq[word] = self.indexReader.CollectionFreq(word)
        return self.corpus_term_freq[word]
    
          