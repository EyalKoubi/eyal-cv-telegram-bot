from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InputFile
import os
TOKEN = os.environ["TOKEN"]

sessions = {}

def start(update, context):
    user_id = update.message.chat_id
    sessions[user_id] = {"step": 1}
    update.message.reply_text("היי! איזה תפקיד אתה מחפש?\n1. מפתח תוכנה\n2. מפתח תוכנה fullStack\n3. אחר")

def handle_message(update, context):
    user_id = update.message.chat_id
    text = update.message.text.strip()

    if user_id not in sessions:
        update.message.reply_text("שלח /start כדי להתחיל את התהליך")
        return

    step = sessions[user_id]["step"]

    if step == 1:
        if text == "1" or text == "2":
            sessions[user_id]["step"] = 2
            update.message.reply_text("כמה שנות ניסיון אתה מחפש?\n1. 0-1\n2. 1-2\n3. יותר")
        elif text == "3":
            del sessions[user_id]
            update.message.reply_text("תודה רבה, אבל כנראה שזה פחות רלוונטי. בהצלחה! 🙏")
        else:
            update.message.reply_text("אנא בחר 1, 2 או 3 🙏")

    elif step == 2:
        if text in ["1", "2", "3"]:
            sessions[user_id]["step"] = 3
            update.message.reply_text("היכן העבודה?\n1. צפון\n2. מרכז\n3. דרום\n4. חו\"ל")
        else:
            update.message.reply_text("אנא בחר 1, 2 או 3 🙏")

    elif step == 3:
        if text == "1" or text == "2":
            sessions[user_id]["step"] = 4
            update.message.reply_text("מה סוג המשרה?\n1. מלאה\n2. חלקית")
        elif text == "3" or text == "4":
            del sessions[user_id]
            update.message.reply_text("נראה שזה פחות מתאים כרגע. תודה ויום נפלא! 🌞")
        else:
            update.message.reply_text("אנא בחר 1, 2, 3 או 4 🙏")

    elif step == 4:
        if text == "1":
            sessions[user_id]["step"] = 5
            update.message.reply_text("איזה סוג עובד אתה מחפש?\n1. עצלן\n2. לא חכם במיוחד\n3. לא אוהב לתכנת\n4. חרוץ ובעל מוטיבציה גבוהה")
        elif text == "2":
            del sessions[user_id]
            update.message.reply_text("נשמע שזה פחות יתאים. בהצלחה בהמשך הדרך! 👋")
        else:
            update.message.reply_text("אנא בחר 1 או 2 🙏")

    elif step == 5:
        if text == "4":
            del sessions[user_id]
            update.message.reply_text("""נשמע שיש התאמה! 🙌
הנה הפרטים שלי:
שם: אייל קובי
📧 eyal4845@gmail.com
📱 0509596599""")
            # שליחת קובץ ה-CV
            with open("cv.pdf", "rb") as pdf_file:
                context.bot.send_document(chat_id=user_id, document=InputFile(pdf_file), filename="cv.pdf")
        elif text in ["1", "2", "3"]:
            del sessions[user_id]
            update.message.reply_text("אז כנראה שלא נסתדר 🙂 שיהיה בהצלחה!")
        else:
            update.message.reply_text("אנא בחר 1, 2, 3 או 4 🙏")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("🤖 הבוט מחכה להודעות...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
