from langchain.document_loaders import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os
import config
os.environ["HUGGINGFACEHUB_API_TOKEN"] = config.HUGGING_FACE_TOKEN
class FAQmanager:
    def load_file(self,file):
        loader = CSVLoader(file,encoding="UTF-8")
        self.document = loader.load()
        self.embeddings = HuggingFaceEmbeddings()
        self.db = FAISS.from_documents(self.document,self.embeddings)

    def similarity_search(self,query):
        search = self.db.similarity_search(query)
        print(type(search))
        return search

