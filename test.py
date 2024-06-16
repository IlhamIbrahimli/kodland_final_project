import speech_recognition as sr

path = r"ready\7daa7c9b-b9a9-4364-a3f9-c1d417fb3bea.wav"


print("Balls")
print(path)
r = sr.Recognizer()
print(r)
with sr.AudioFile(path) as source:
    audio_data = r.record(source)
print(audio_data)
text = r.recognize_google(audio_data, language="ru-RU")
print(text)
