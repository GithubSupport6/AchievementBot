from pydoc import describe
from unicodedata import name
import telebot
from entities import Achievement
from sqlalchemy.orm import Session
from sqlalchemy import select
from entities import User
from entities import init_db

bot = telebot.TeleBot('5562135400:AAHj8dPpvdIrmfwbps8aVZ3iGOmzpCjKyD0')
admin_id = [869853516,1799239576]
engine = init_db()

@bot.message_handler(commands=['add'])
def add_handler(message):
    if (message.from_user.id in admin_id):
        bot.send_message(message.from_user.id, "Введите название")
        bot.register_next_step_handler(message,get_name)
    else:
        bot.send_message(message.from_user.id, "Пашел нахуй")


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Введите описание")
    bot.register_next_step_handler(message,get_description)

def get_description(message):
    global description
    description = message.text
    achievement = Achievement(
        name,
        description
    )

    user = find_user(message.from_user.id)
    if (user == None):
        user = add_user(message.from_user.id)

    print(user.id)
    add_achievement(user.id,achievement)
    bot.send_message(message.from_user.id, "Создано успешно")
   
def find_user(id):
    with Session(engine) as session:
        session.expire_on_commit = False
        user = session.query(User).filter(User.id == id).first()
        session.commit()
        session.expunge(user)
        return user
        

def add_user(id):
    with Session(engine) as session:
        user = User(
            id = id
        )
        session.add(user)
        session.commit()
        return user

def add_achievement(id, achievement):
    with Session(engine) as session:
        session.expire_on_commit = False
        session.add(achievement)
        user_for_achievement = session.query(User).filter(User.id == id).first()
        user_for_achievement.achievements.append(achievement)
        session.add(user_for_achievement)
        session.commit()
        return achievement

def get_all_achievements(userid):
    with Session(engine) as session:
        user = select(User).where(User.id == userid)
        s = session.query(Achievement).filter(user in Achievement.users).all()
        session.commit()
        return s

@bot.message_handler(commands=['getAchievements'])
def add_handler(message):
    achievements = get_all_achievements(message.from_user.id)
    for achievement in achievements:
        msg = "(" + str(achievement.userid) + "," + achievement.name + "," + achievement.description + ")"
        bot.send_message(message.from_user.id, msg)

bot.polling(none_stop=True, interval=0)