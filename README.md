# Telegram Reminder Bot

## Description
This project is a simple Telegram bot that sends reminders to users. 

## Technologies
- Python
- SQLite
- Flask (if used)
- Git

## Features
- Add new reminders with custom text and date/time
- View and manage stored reminders (list, edit, delete)
- Restore pending reminders from the database after restart
- Send timely notifications to users when reminders are due

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/kurseasy/telegram-bot-reminder
   cd telegram-bot-reminder
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Create a file named .env and add your Telegram Bot token:
   ```bash
   TELEGRAM_TOKEN=your_token_here
4. Run the bot:
   ```bash
   python bot.py

