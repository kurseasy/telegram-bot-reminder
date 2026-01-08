import os
import sqlite3
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

conn = sqlite3.connect("reminders.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders_once (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    remind_datetime TEXT
)
""")
conn.commit()

def start(update, context):
    update.message.reply_text(
        "Привет! Используй /addonce <YYYY-MM-DD HH:MM> <текст> для разового напоминания.\n"
        "Например: /addonce 2026-01-10 09:30 Сдать отчёт."
    )

def addonce(update, context):
    user_id = update.effective_user.id
    if len(context.args) < 3:
        update.message.reply_text("Формат: /addonce YYYY-MM-DD HH:MM текст")
        return

    datetime_str = " ".join(context.args[:2])
    text = " ".join(context.args[2:])

    try:
        remind_dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        update.message.reply_text("Неверный формат. Используй YYYY-MM-DD HH:MM")
        return

    cursor.execute("INSERT INTO reminders_once (user_id, text, remind_datetime) VALUES (?, ?, ?)", 
                   (user_id, text, datetime_str))
    conn.commit()

    context.job_queue.run_once(
        send_once_reminder,
        when=remind_dt,
        context=(user_id, text)
    )

    update.message.reply_text(f"Добавлено разовое напоминание: {text} на {datetime_str}")

def send_once_reminder(context):
    user_id, text = context.job.context
    context.bot.send_message(chat_id=user_id, text=f"🔔 Разовое напоминание: {text}")

def list_once(update, context):
    user_id = update.effective_user.id
    cursor.execute("SELECT id, text, remind_datetime FROM reminders_once WHERE user_id=?", (user_id,))
    items = cursor.fetchall()
    if not items:
        update.message.reply_text("У тебя пока нет разовых напоминаний.")
        return
    formatted = "\n".join(f"{row[0]}. {row[1]} (в {row[2]})" for row in items)
    update.message.reply_text(f"Твои разовые напоминания:\n{formatted}")

def delete_once(update, context):
    user_id = update.effective_user.id
    if not context.args or not context.args[0].isdigit():
        update.message.reply_text("Укажи ID для удаления: /deleteonce 1")
        return
    reminder_id = int(context.args[0])
    cursor.execute("DELETE FROM reminders_once WHERE id=? AND user_id=?", (reminder_id, user_id))
    conn.commit()
    if cursor.rowcount == 0:
        update.message.reply_text("Неверный ID или напоминание не найдено.")
    else:
        update.message.reply_text(f"Разовое напоминание {reminder_id} удалено.")

def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN не найден. Создай .env с TELEGRAM_TOKEN=твой_токен")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addonce", addonce))
    dp.add_handler(CommandHandler("listonce", list_once))
    dp.add_handler(CommandHandler("deleteonce", delete_once))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

