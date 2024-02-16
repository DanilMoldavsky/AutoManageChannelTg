from telebot import types
from rewriter.rewrite_gpt import GptRewriter
from db.sqllite_main import SQLite
import telebot
import time


# Часть с ботом
bot = telebot.TeleBot('YOUR TOKEN')
db = SQLite("db\\users.db")
table = db.table
ID_PERS = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    full = types.KeyboardButton('Полный скрипт')
    srap = types.KeyboardButton('Посмотреть посты')
    rew = types.KeyboardButton('Рерайт через GPT')
    send = types.KeyboardButton('Отправить пост в телеграм канал')
    markup.add(full, srap, rew, send)#, btn2
    bot.send_message(message.chat.id, '''👋 Привет!
💎 С помощью этого бота ты сможешь парсить, рерайтить и постить посты из тг!
                     ''',  reply_markup=markup)


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    bot.send_message(message.chat.id, f'Приветствую нового человека! {message.chat.id}')


@bot.message_handler(commands=['myid'])
def send_id(message):
    bot.send_message(message.from_user.id, f'{message.from_user.id}')
    

@bot.message_handler(content_types=['text'])
def get_user_text(message, db=SQLite("db\\02.02.db")):
    global table
    global ID_PERS
    global ID_MESSAGE_EDIT
    
    db=SQLite("db\\02.02.db")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    full = types.KeyboardButton('Полный скрипт')
    srap = types.KeyboardButton('Посмотреть посты')
    rew = types.KeyboardButton('Рерайт через GPT')
    send = types.KeyboardButton('Отправить пост в телеграм канал')
    markup.add(full, srap, rew, send)
    
    markup_posts = types.ReplyKeyboardMarkup(resize_keyboard=True)
    look = types.KeyboardButton('Посмотреть посты')
    hide = types.KeyboardButton('Посмотреть только кол-во постов')
    markup_posts.add(look, hide)
    
    markup_gpt = types.ReplyKeyboardMarkup(resize_keyboard=True)
    look_gpt = types.KeyboardButton('Посмотреть посты от GPT')
    hide_gpt = types.KeyboardButton('Посмотреть только кол-во постов от GPT')
    markup_gpt.add(look_gpt, hide_gpt)
    
    markup_gpt_delete = types.ReplyKeyboardMarkup(resize_keyboard=True)
    all_gpt_delete = types.KeyboardButton('Удалить все посты от GPT')
    start = types.KeyboardButton('/start')
    markup_gpt_delete.add(all_gpt_delete, start)
    
    markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = types.KeyboardButton('/start')
    markup_start.add(start)
    
    if message.text.lower() == "полный скрипт":
        for i in range(5):
            print(i)
            
    elif message.text.lower() == "посмотреть посты":
        db.take_alltables()
        list_cnt = [id + 1 for id, num in db.rows]
        
        markup_check_tables = types.ReplyKeyboardMarkup(resize_keyboard=True)
        list_btn_posts = [types.KeyboardButton(f'Таблица "{choice}"') for choice in db.name_tables]
        start = types.KeyboardButton('/start')
        markup_check_tables.add(*list_btn_posts, start)
        
        bot.send_message(message.chat.id, 'Из какой таблицы нужны записи?', reply_markup=markup_check_tables)
        
    elif message.text.lower()[:7] == "таблица":
        ID_PERS = message.from_user.id
        
        check_word = 'таблица "'
        table = ''
        for c in message.text.lower():
            if c not in check_word:
                table += c
                
        db.take_all(table)
        
        list_cnt = [id + 1 for id, num in db.rows]
        
        markup_chek_table = types.ReplyKeyboardMarkup(resize_keyboard=True)
        list_btn_posts = [types.KeyboardButton(f'{choice} пост') for choice in list_cnt]
        delete_all = types.KeyboardButton('Удалить все')
        markup_chek_table.add(*list_btn_posts, delete_all)
        bot.send_message(message.chat.id, 'Какие посты нужны?', reply_markup=markup_chek_table)
    
    elif message.text.lower()[2:] in "удалить все":
        db.delete_all(table)
        db.take_all(table)
        
        bot.send_message(message.chat.id, f'Бд очищена, стол {table} включает {len(db.rows)} постов', reply_markup=markup_start)
        
    
    elif message.text.lower()[2:] in "посты":
        markup_edit_del = types.ReplyKeyboardMarkup(resize_keyboard=True)
        edit_btn = types.KeyboardButton('Редактировать пост')
        delete_btn = types.KeyboardButton('Удалить пост')
        markup_edit_del.add(edit_btn, delete_btn)
        
        db.take_all(table)
        db.rows_text = [el for id, el in db.rows]
        db.show_post = (int(message.text.lower()[0]) - 1, db.rows_text[int(message.text.lower()[0]) - 1])
        ID_MESSAGE_EDIT = db.show_post[0]
        

        bot.send_message(message.chat.id, f'"{db.show_post[1]}"\n\nЭтот пост выбран. *Редактировать* или *удалить*?', reply_markup=markup_edit_del, parse_mode="Markdown")
    
    elif message.text.lower() == "удалить пост":
        db.take_all(table)
        for id, el in db.rows:
            if id == ID_MESSAGE_EDIT:
                db.delete(table=table, id=id)
        db.take_all(table)
        bot.send_message(ID_PERS, f'Пост удален, в таблице *{table}*, осталось `{len(db.rows)} постов`', reply_markup=markup_start, parse_mode="Markdown")
    
    elif message.text.lower() == "редактировать пост":
        bot.send_message(ID_PERS, 'Ответьте на это сообщение уже отредактированным постом\n_Обязательно в ковычках!_', parse_mode="Markdown")
        
    elif '"' in message.text.lower():
        db.take_all(table)
        for id, el in db.rows:
            if id == ID_MESSAGE_EDIT:
                db.update(table=table, post=message.text.lower(), id=id)
        bot.send_message(ID_PERS, '`Пост обновлен и добавлен в бд`', reply_markup=markup_start, parse_mode="Markdown")
    
    
    elif message.text.lower() == "рерайт через gpt":
        db = SQLite("db\\02.02.db")
        db.take_all("scrape")
        # db.create_table("rewrite")
        
        data = [el for id, el in db.rows]
        gpt = GptRewriter(data)
        bot.send_message(message.chat.id, f'{len(data)} постов для рерайта, пожалуйста подождите...', )
        gpt.rewrite()
        db.create_table_if_not("rewrite")
        for id, el in enumerate(gpt.output):
            db.insert(table="rewrite", id=id, post=el)
        bot.send_message(message.chat.id, f'Посты успешно переписаны и отправлены в бд', reply_markup=markup_gpt)
        
    elif message.text.lower() == "посмотреть посты от gpt":
        db = SQLite("db\\02.02.db")
        db.take_all("rewrite")
        for id, el in db.rows:
            bot.send_message(message.chat.id, el, reply_markup=markup_gpt_delete)
            
    elif message.text.lower() == "посмотреть только кол-во постов от gpt":
        db = SQLite("db\\02.02.db")
        db.take_all("rewrite")
        bot.send_message(message.chat.id, f'{len(db.rows)} постов после рерайта в бд', reply_markup=markup_gpt_delete)
    
    elif message.text.lower() == "удалить все посты от gpt":
        db = SQLite("db\\02.02.db")
        db.delete_all("rewrite")
        db.take_all("rewrite")
        print(len(db.rows))
        bot.send_message(message.chat.id, f'Бд очищена, стол rewrite включает {len(db.rows)} постов', reply_markup=markup_start)


    elif message.text.lower() == "отправить пост в телеграм канал":
        db = SQLite("db\\02.02.db")
        db.take_all("rewrite")
        
        list_cnt = [id + 1 for id, num in db.rows]
        
        markup_chek_posts = types.ReplyKeyboardMarkup(resize_keyboard=True)
        list_btn_posts = [types.KeyboardButton(f'{choice} пост') for choice in list_cnt]
        
        send_all = types.KeyboardButton('Отправить все посты')
        markup_chek_posts.add(*list_btn_posts, send_all)
        
        bot.send_message(message.chat.id, f'Выберите какой именно пост вы хотите отправить или выберите команду - Отправить все', reply_markup=markup_chek_posts)

    elif message.text.lower() == "отправить все посты":
        db = SQLite("db\\02.02.db")
        db.take_all("rewrite")
        
        for id, el in db.rows:
            bot.send_message('@pon4ik_channel', el)
            time.sleep(2)


if __name__ == '__main__':
    bot.polling(none_stop=True)
