import os
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Simple in-memory storage for reminders
reminders = {}

def start(update, context):
    update.message.reply_text("Hi! Use /add <text> to add a reminder. Use /list to see all reminders.")

def add(update, context):
    user_id = update.effective_user.id
    text = " ".join(context.args).strip()
    if not text:
        update.message.reply_text("Please provide reminder text: /add Buy milk")
        return
    reminders.setdefault(user_id, [])
    reminders[user_id].append(text)
    update.message.reply_text(f"Added reminder: {text}")

def list_cmd(update, context):
    user_id = update.effective_user.id
    items = reminders.get(user_id, [])
    if not items:
        update.message.reply_text("No reminders yet.")
        return
    formatted = "\n".join(f"{i+1}. {r}" for i, r in enumerate(items))
    update.message.reply_text(f"Your reminders:\n{formatted}")

def delete(update, context):
    user_id = update.effective_user.id
    items = reminders.get(user_id, [])
    if not items:
        update.message.reply_text("No reminders to delete.")
        return
    if not context.args or not context.args[0].isdigit():
        update.message.reply_text("Please provide an ID to delete: /delete 1")
        return
    idx = int(context.args[0]) - 1
    if idx < 0 or idx >= len(items):
        update.message.reply_text("Invalid ID.")
        return
    removed = items.pop(idx)
    update.message.reply_text(f"Deleted: {removed}")

def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN not found. Create .env with TELEGRAM_TOKEN=your_token")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("list", list_cmd))
    dp.add_handler(CommandHandler("delete", delete))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
