import logic
man = logic.FAQmanager()

man.load_file("FAQ.csv")
print(man.similarity_search("Что делать, если товар пришел поврежденным?"))