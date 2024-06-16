import logic
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
import uuid
import os

man = logic.FAQmanager()
man.load_file("FAQ.csv")
bot = TeleBot(TELEBOT_API)



def gen_markup_for_text():
        markup = InlineKeyboardMarkup()
        markup.row_width = 1

        markup.add(InlineKeyboardButton('Да', callback_data='transfer'),
                   InlineKeyboardButton('Нет', callback_data='no_transfer'))
        
        return markup

@bot.message_handler(content_types=["voice"])
def audio_question(message):
    filename = str(uuid.uuid4())
    file_name_full='voice/'+filename+'.ogg'
    file_name_full_converted = 'ready/'+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)

    text = man.recognise_audio(file_name_full_converted)

    os.remove(file_name_full)
    os.remove(file_name_full_converted)
    print(text)
    text = man.similarity_search(text)
    answer = man.parse_text(text)
    if answer == "Либо ваш ответ слишком сложен для меня, либо я не понял, что вы сказали. Хотите поговорить с профессионалом?":
        bot.send_message(message.chat.id,answer, reply_markup=gen_markup_for_text())
    else:
        bot.send_message(message.chat.id,answer)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    if call.data == "transfer":
        bot.send_message(call.message.chat.id, "Передача к профессионалу. Пожалуйста, подождите...")
            
    elif call.data == "no_transfer":
        bot.send_message(call.message.chat.id,  "Повторите, пожалуйста, то, что вы хотели спросить.")



@bot.message_handler(func=lambda message: True)
def text_question(message):
    text = man.similarity_search(message.text)
    answer = man.parse_text(text)
    bot.send_message(message.chat.id,answer)
    if answer == "Либо ваш ответ слишком сложен для меня, либо я не понял, что вы сказали. Хотите поговорить с профессионалом?":
        bot.send_message(message.chat.id,answer, reply_markup=gen_markup_for_text())
    else:
        bot.send_message(message.chat.id,answer)

bot.infinity_polling()
