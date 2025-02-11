import telebot
from telebot import types
import os
import requests
import logging

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Используем переменную окружения для токена
BITRIX_WEBHOOK_URL = os.getenv("BITRIX_WEBHOOK_URL")  # Вебхук Битрикс24
OPENLINE_ID = os.getenv("BITRIX_OPENLINE_ID")  # ID открытой линии Битрикс24

bot = telebot.TeleBot(TOKEN)

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Словарь соответствия пользователей и чатов в Битрикс24
user_sessions = {}

# Функция отправки сообщения в Битрикс24
def send_to_bitrix(chat_id, message_text):
    user_info = bot.get_chat(chat_id)  # Получаем информацию о пользователе
    
    # Проверяем, есть ли у пользователя открытый диалог
    if chat_id not in user_sessions:
        response = requests.get(f"{BITRIX_WEBHOOK_URL}imopenlines.dialog.list.json")
        if response.status_code == 200 and "result" in response.json():
            # Создаём новый чат с пользователем
            data = {
                "USER_ID": f"telegram_{chat_id}",
                "LINE_ID": OPENLINE_ID,
                "USERNAME": user_info.first_name,
                "AVATAR": user_info.photo if user_info.photo else ""
            }
            chat_response = requests.post(f"{BITRIX_WEBHOOK_URL}imopenlines.dialog.add.json", json=data)
            if chat_response.status_code == 200 and "result" in chat_response.json():
                user_sessions[chat_id] = chat_response.json()["result"]["DIALOG_ID"]

    # Отправляем сообщение в чат
    if chat_id in user_sessions:
        message_data = {
            "DIALOG_ID": user_sessions[chat_id],
            "MESSAGE": message_text
        }
        response = requests.post(f"{BITRIX_WEBHOOK_URL}imopenlines.message.add.json", json=message_data)

        if response.status_code == 200:
            return True
        else:
            logger.error(f"Ошибка при отправке в Битрикс24: {response.text}")
            return False

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    chat_id = message.chat.id
    text = message.text

    # Отправляем сообщение в Битрикс24
    if send_to_bitrix(chat_id, text):
        bot.send_message(chat_id, "Ваше сообщение передано оператору Битрикс24. Ожидайте ответа.")
    else:
        bot.send_message(chat_id, "Ошибка при отправке в Битрикс24. Попробуйте позже.")

# Обработчик фото и документов
@bot.message_handler(content_types=['photo', 'document'])
def handle_media_message(message):
    chat_id = message.chat.id

    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id  # Берем фото в наилучшем качестве
    else:
        file_id = message.document.file_id

    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

    message_text = f"📎 Пользователь отправил файл: {file_url}"

    if send_to_bitrix(chat_id, message_text):
        bot.send_message(chat_id, "Файл передан оператору Битрикс24.")
    else:
        bot.send_message(chat_id, "Ошибка при отправке файла в Битрикс24.")

# Обработчик ответов из Битрикс24
def get_messages_from_bitrix():
    response = requests.get(f"{BITRIX_WEBHOOK_URL}imopenlines.message.get.json")

    if response.status_code == 200 and "result" in response.json():
        messages = response.json()["result"]

        for msg in messages:
            user_id = msg["USER_ID"]
            text = msg["MESSAGE"]

            # Ищем пользователя в Telegram
            for chat_id, dialog_id in user_sessions.items():
                if dialog_id == user_id:
                    bot.send_message(chat_id, f"👨‍💼 Оператор: {text}")

# Функция для проверки новых сообщений
def check_new_messages():
    while True:
        get_messages_from_bitrix()
        time.sleep(10)  # Проверяем каждые 10 секунд


# Главное меню
def main_menu():
    markup = types.InlineKeyboardMarkup()
    living = types.InlineKeyboardButton("Проживание", callback_data='living')
    restoran = types.InlineKeyboardButton("Ресторан", callback_data='restoran')
    spa = types.InlineKeyboardButton("СПА", callback_data='spa')
    medicine = types.InlineKeyboardButton("Медицина", callback_data='medicine')
    loyality = types.InlineKeyboardButton("Программа лояльности ЛОГУС", callback_data='loyality')
    markup.add(living)  # Каждая кнопка на новой строке
    markup.add(restoran)
    markup.add(spa)
    markup.add(medicine)
    markup.add(loyality)
    return markup

# Подменю для "Проживание"
def living_menu():
    markup = types.InlineKeyboardMarkup()
    tech_problem = types.InlineKeyboardButton("Технические проблемы", callback_data='tech_problem')
    living_option2 = types.InlineKeyboardButton("Цены", callback_data='living_option2')
    living_back = types.InlineKeyboardButton("Назад в главное меню", callback_data='main_menu')
    markup.add(tech_problem)  # Каждая кнопка на новой строке
    markup.add(living_option2)
    markup.add(living_back)
    return markup

# Подменю для "Технические проблемы"
def tech_problem_menu():
    markup = types.InlineKeyboardMarkup()
    electric_problem = types.InlineKeyboardButton("Проблемы с электричеством", callback_data='electric_problem')
    water_problem = types.InlineKeyboardButton("Проблемы с водоснабжением", callback_data='water_problem')
    temp_problem = types.InlineKeyboardButton("Некомфортная температура в номере", callback_data='temp_problem')
    safe_problem = types.InlineKeyboardButton("Проблемы с сейфом", callback_data='safe_problem')
    tv_problem = types.InlineKeyboardButton("Неисправен ТВ", callback_data='tv_problem')
    another_problem = types.InlineKeyboardButton("Другой вопрос", callback_data='another_problem')
    tech_problem_back = types.InlineKeyboardButton("Назад", callback_data='tech_problem_back')
    markup.add(electric_problem)
    markup.add(water_problem)
    markup.add(temp_problem)
    markup.add(safe_problem)
    markup.add(tv_problem)
    markup.add(another_problem)
    markup.add(tech_problem_back)
    return markup

#Подменю для "Проблемы с электричеством"
def electric_problem_menu():
    markup = types.InlineKeyboardMarkup()
    electric_problem_menu_back = types.InlineKeyboardButton("Назад", callback_data='electric_problem_menu_back')
    markup.add(electric_problem_menu_back)
    return markup

#Подменю для "Проблемы с водоснабжением"
def water_problem_menu():
    markup = types.InlineKeyboardMarkup()
    water_problem_menu_back = types.InlineKeyboardButton("Назад", callback_data='water_problem_menu_back')
    markup.add(water_problem_menu_back)
    return markup


# Подменю для "Ресторан"
def restoran_menu():
    markup = types.InlineKeyboardMarkup()
    restoran_work_time = types.InlineKeyboardButton("Время работы кофейни и ресторана", callback_data='restoran_work_time')
    restoran_eat_menu = types.InlineKeyboardButton("Меню ресторана\рум-сервиса", callback_data='restoran_eat_menu')
    restoran_order = types.InlineKeyboardButton("Оформить заказ в номер", callback_data='restoran_order')
    restoran_back = types.InlineKeyboardButton("назад", callback_data='restoran_back')
    markup.add(restoran_work_time)  
    markup.add(restoran_eat_menu)
    markup.add(restoran_order)
    markup.add(restoran_back)
    return markup

# Подменю СПА
def spa_menu():
    markup = types.InlineKeyboardMarkup()
    spa_bron = types.InlineKeyboardButton("Бронирование услуг", callback_data='spa_bron')
    spa_menu_check = types.InlineKeyboardButton("Меню", callback_data='spa_menu_check')
    spa_call_manager = types.InlineKeyboardButton("Связь с менеджером", callback_data='spa_call_manager')
    spa_skidki = types.InlineKeyboardButton("Акции", callback_data='spa_skidki')
    spa_route = types.InlineKeyboardButton("Как добраться?", callback_data='spa_route')
    spa_call_back = types.InlineKeyboardButton("Оставить отзыв", callback_data='spa_call_back')
    spa_back = types.InlineKeyboardButton("назад", callback_data='spa_back')
    markup.add(spa_bron)
    markup.add(spa_menu_check)
    markup.add(spa_call_manager)
    markup.add(spa_skidki)
    markup.add(spa_route)
    markup.add(spa_call_back)
    markup.add(spa_back)
    return markup

# Подменю для Программы лояльности
def loyality_menu():
    markup = types.InlineKeyboardMarkup()
    loyality_register = types.InlineKeyboardButton("Зарегистрироваться", url="https://loyalty.donresort.ru/")
    loyality_privileges = types.InlineKeyboardButton("Привилегии участников программы", callback_data='loyality_privileges',)
    loyality_rules = types.InlineKeyboardButton("Правила участия в программе лояльности", callback_data='loyality_rules')
    loyality_back = types.InlineKeyboardButton("назад", callback_data='loyality_back')
    markup.add(loyality_register)
    markup.add(loyality_privileges)
    markup.add(loyality_rules)
    markup.add(loyality_back)
    return markup
    
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в Санаторий Дон! Выберите интересующую вас категорию в меню ниже",
        reply_markup=main_menu()
    )
# обработчики нажатия кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Проживание
    if call.data == 'living':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Вы выбрали 'Проживание'. Выберите подкатегорию:",
            reply_markup=living_menu()
        )
    # Ресторан    
    elif call.data == 'restoran':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Вы выбрали 'Ресторан'. Выберите подкатегорию:",
            reply_markup=restoran_menu()
        )
    # СПА    
    elif call.data == 'spa':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Вы выбрали 'Спа'. Выберите подкатегорию:",
            reply_markup=spa_menu()
        )  
     # Программа лояльности    
    elif call.data == 'loyality':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Вы выбрали 'Программа лояльности ЛОГУС'. Выберите подкатегорию:",
            reply_markup=loyality_menu()
        )
    
    # Возврат из меню Программа лояльности в главное меню
    elif call.data == 'loyality_back':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Добро пожаловать в Санаторий Дон! Выберите интересующую вас категорию в меню ниже",
            reply_markup=main_menu()
        )
              
    # Возврат из меню Ресторан в главное меню
    elif call.data == 'restoran_back':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Добро пожаловать в Санаторий Дон! Выберите интересующую вас категорию в меню ниже",
            reply_markup=main_menu()
        )
    
    # Технические проблемы
    elif call.data == 'tech_problem':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Уточните, какие наблюдаются проблемы",
            reply_markup=tech_problem_menu()
        )
    # Главное меню
    elif call.data == 'main_menu':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Добро пожаловать в Санаторий Дон! Выберите интересующую вас категорию в меню ниже",
            reply_markup=main_menu()
        )
    # Возврат из меню Техпроблемы в меню Проживание
    elif call.data == 'tech_problem_back':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Вы выбрали 'Проживание'. Выберите подкатегорию:",
            reply_markup=living_menu()
        )    
    # Проблемы с электричеством
    elif call.data == 'electric_problem':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Направлена предварительная заявка. С Вами свяжутся",
            reply_markup=electric_problem_menu()
            )
    # Возврат из меню Электричество в меню Проживание
    elif call.data == 'electric_problem_menu_back':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Вы выбрали 'Проживание'. Выберите подкатегорию:",
            reply_markup=living_menu()
        )
    # Проблемы с водоснабжением
    elif call.data == 'water_problem':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Направлена предварительная заявка. С Вами свяжутся",
            reply_markup=water_problem_menu()
            )
    # Возврат из меню Водоснабжение в меню Проживание
    elif call.data == 'water_problem_menu_back':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Вы выбрали 'Проживание'. Выберите подкатегорию:",
            reply_markup=living_menu()
        )
    # Возврат из меню СПА в главное меню
    elif call.data == 'spa_back':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Добро пожаловать в Санаторий Дон! Выберите интересующую вас категорию в меню ниже",
            reply_markup=main_menu()
        )
    
        
# Обработчик для удаления текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # Удаляем сообщение пользователя
    bot.delete_message(message.chat.id, message.message_id)
    # Отправляем предупреждение
    bot.send_message(
        message.chat.id,
        "Пожалуйста, используйте кнопки для взаимодействия с ботом.",
        reply_markup=main_menu()
    )        

bot.infinity_polling()