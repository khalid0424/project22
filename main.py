import telebot
import requests

TOKEN = "secret"
bot = telebot.TeleBot(TOKEN)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.reply_to(message, "Салом! Ман боти коркарди матн бо Llama2 мебошам. Матни худро фиристед!")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Хатогӣ дар ирсоли паёми истиқбол: {e}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    data = {
        "model": "llama3.2",
        "prompt": message.text,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=data)
        response.raise_for_status()  
        response_text = response.json().get('response', "Аз модел ҷавобе нест.")
        
        
        bot.reply_to(message, response_text)
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, "Бубахшед, ман ба сервер дастрасӣ надорам. Лутфан баъдтар кӯшиш кунед.")
        print(f"Хатогии дархост: {e}")
    except telebot.apihelper.ApiTelegramException as e:
        if "403" in str(e):
            print("Бот аз ҷониби корбар баста шуд.")
        elif "400" in str(e):
            print("Паёми ҷавобнаёфта.")
        else:
            print(f"Хатогии API-и Telegram: {e}")
    except Exception as e:
        bot.reply_to(message, f"Бубахшед, хатое рух дод: {str(e)}")
        print(f"Хатогии ғайричашмдошт: {e}")


print("Бот фаъол аст...")
bot.infinity_polling()
