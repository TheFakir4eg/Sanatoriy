import telebot
from telebot import types
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Используем переменную окружения для токена
bot = telebot.TeleBot(TOKEN)

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