import os
import telebot
from telebot import types
from groq import Groq

# استدعاء المفاتيح من إعدادات السيرفر للأمان
TELEGRAM_TOKEN = os.environ.get("9086019429:AAH5NsEKkCvsdt2WtZ6rUkny3VxrHtF2SxA")
GROQ_API_KEY = os.environ.get ("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")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# رسالة الترحيب والقائمة الرئيسية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🐍 ملخصات البايثون والبرمجة")
    btn2 = types.KeyboardButton("💰 ملخصات الثقافة المالية")
    btn3 = types.KeyboardButton("📝 امتحانات سابقة")
    btn4 = types.KeyboardButton("📢 تواصل معنا / إعلانات")
    markup.add(btn1, btn2, btn3, btn4)
    
    welcome_text = (
        "أهلاً بيك يا بطل في مساعد تانية بكالوريا! 🎓\n\n"
        "تقدر تختار من القائمة تحت لو عاوز ملخصات جاهزة، أو **اكتب سؤالك مباشرة هنا** "
        "(سواء مسألة ثقافة مالية أو كود بايثون) وهحلهولك وأشرحهولك فوراً! 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# الرد على أزرار القائمة (هنا تقدر تحط روابط قنواتك أو ملازمك)
@bot.message_handler(func=lambda message: message.text in [
    "🐍 ملخصات البايثون والبرمجة", 
    "💰 ملخصات الثقافة المالية", 
    "📝 امتحانات سابقة", 
    "📢 تواصل معنا / إعلانات"
])
def handle_menu(message):
    if message.text == "🐍 ملخصات البايثون والبرمجة":
        bot.reply_to(message, "📚 هنا تقدر تحط رابط قناة التليجرام أو جوجل درايف اللي فيه ملخصات البايثون.\n(أو اسألني أي سؤال في البرمجة دلوقتي!)")
    elif message.text == "💰 ملخصات الثقافة المالية":
        bot.reply_to(message, "📊 هنا تقدر تحط ملخصات قوانين الثقافة المالية.\n(أو ابعت أي مسألة مالية وهحلهالك بالخطوات!)")
    elif message.text == "📝 امتحانات سابقة":
        bot.reply_to(message, "📝 جاري تجميع أحدث نماذج الامتحانات... تابع قناتنا عشان توصلك أول بأول!")
    elif message.text == "📢 تواصل معنا / إعلانات":
        bot.reply_to(message, "للحصول على الملازم النهائية أو للإعلان داخل البوت، تواصل مع الإدارة: @YourUsername")

# الرد بالذكاء الاصطناعي على أي سؤال يكتبه الطالب
@bot.message_handler(func=lambda message: True)
def ask_ai(message):
    # إظهار علامة "يكتب الآن..."
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "أنت مدرس خبير لطلاب الصف الثاني الثانوي (تانية بكالوريا في مصر) في مواد البرمجة، "
                        "لغة بايثون (Python)، والثقافة المالية. اشرح الإجابات باللغة العربية بأسلوب مبسط وواضح ومرتب. "
                        "إذا كان السؤال كود بايثون، اكتب الكود الصحيح واشرح كل سطر ببساطة. "
                        "إذا كانت مسألة ثقافة مالية، اكتب القانون ثم خطوات الحل ثم الناتج النهائي."
                    )
                },
                {
                    "role": "user",
                    "content": message.text,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        reply = chat_completion.choices[0].message.content
        
        # إضافة سطر إعلاني صغير في نهاية كل إجابة للربح
        ad_footer = "\n\n━━━━━━━━━━━━━━\n💡 *تابع قناتنا للمراجعات النهائية:* @YourChannel"
        
        bot.reply_to(message, reply + ad_footer, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, "معلش حصل ضغط بسيط، جرب تبعت سؤالك تاني كمان ثواني! 🙏")

print("Bot is running...")
bot.infinity_polling()
