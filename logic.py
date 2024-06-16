from langchain.document_loaders import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os
import config
import speech_recognition as sr


os.environ["HUGGINGFACEHUB_API_TOKEN"] = config.HUGGING_FACE_TOKEN
class FAQmanager:
    def load_file(self,file):
        loader = CSVLoader(file,encoding="UTF-8")
        self.document = loader.load()
        self.embeddings = HuggingFaceEmbeddings()
        self.db = FAISS.from_documents(self.document,self.embeddings)

    def similarity_search(self,query):
        search = self.db.similarity_search_with_score(query)
        print(type(search))
        return search
    
    def parse_text(self,text):
        #
        print(text)
        closest_result = text[0][0].page_content
        if text[0][1] <= 1.2:
            qa_list = closest_result.split("\n")
            answer = qa_list[1]
            answer = answer[7:]
            return answer
        else:
            return "Либо ваш ответ слишком сложен для меня, либо я не понял, что вы сказали. Хотите поговорить с профессионалом?"


    def recognise_audio(self,path):
        try:
            r = sr.Recognizer()
            with sr.AudioFile(path) as source:
                audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="ru-RU")
            return text
        except:
            return "transcription failed."

