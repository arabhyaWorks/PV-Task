import telebot
import threading
import time
import schedule

TOKEN = '7571489564:AAGT8d5Y09nebpg738iilyhzplWq3LhMbuY'

bot = telebot.TeleBot(TOKEN)

# Remove any existing webhook
bot.remove_webhook()

# In-Memory Task List (replace with database for persistent storage)
tasks = []

# Start Command
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "Welcome to Persist Ventures Operations Bot! Use /help to see available commands.")

# Help Command
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Available Commands:\n"
        "/start - Welcome message\n"
        "/help - List available commands\n"
        "/addtask <task> - Add a task\n"
        "/viewtasks - View all tasks\n"
        "/removetask <task> - Remove a specific task\n"
        "/completetask <task> - Mark a task as completed\n"
        "/cleartasks - Clear all tasks\n"
        "/checkin - Mark your daily check-in\n"
        "/checkout - Mark your daily check-out\n"
        "/leave - Request leave for a specific day\n"
        "/leaderboard - View the team leaderboard\n"
        "/taskstatus - Update or view task progress\n"
        "/contact - Get support from the admin team"
    )
    bot.reply_to(message, help_text)

# Add Task Command
@bot.message_handler(commands=['addtask'])
def add_task_command(message):
    task = message.text.replace('/addtask', '').strip()
    if task:
        tasks.append(task)
        bot.reply_to(message, f"✅ Task added: '{task}'")
    else:
        bot.reply_to(message, "❗ Usage: /addtask <task> - Please specify the task to add.")

# View Tasks Command
@bot.message_handler(commands=['viewtasks'])
def view_tasks_command(message):
    if tasks:
        task_list = "\n".join(f"{i + 1}. {task}" for i, task in enumerate(tasks))
        bot.reply_to(message, f"📋 Current Tasks:\n{task_list}")
    else:
        bot.reply_to(message, "No tasks available! Use /addtask to add a new task.")

# Remove Task Command
@bot.message_handler(commands=['removetask'])
def remove_task_command(message):
    task = message.text.replace('/removetask', '').strip()
    if task:
        if task in tasks:
            tasks.remove(task)
            bot.reply_to(message, f"🗑️ Task removed: '{task}'")
        else:
            bot.reply_to(message, "❗ Task not found! Use /viewtasks to see the list of tasks.")
    else:
        bot.reply_to(message, "❗ Usage: /removetask <task> - Please specify the task to remove.")

# Complete Task Command
@bot.message_handler(commands=['completetask'])
def complete_task_command(message):
    task = message.text.replace('/completetask', '').strip()
    if task:
        if task in tasks:
            tasks.remove(task)
            bot.reply_to(message, f"✅ Task completed: '{task}'")
        else:
            bot.reply_to(message, "❗ Task not found! Use /viewtasks to see the list of tasks.")
    else:
        bot.reply_to(message, "❗ Usage: /completetask <task> - Please specify the task to mark as completed.")

# Clear All Tasks Command
@bot.message_handler(commands=['cleartasks'])
def clear_tasks_command(message):
    if tasks:
        tasks.clear()
        bot.reply_to(message, "🧹 All tasks have been cleared!")
    else:
        bot.reply_to(message, "❗ No tasks to clear.")

# New Commands
@bot.message_handler(commands=['checkin'])
def checkin_command(message):
    bot.reply_to(message, "✅ You have successfully checked in for the day!")

@bot.message_handler(commands=['checkout'])
def checkout_command(message):
    bot.reply_to(message, "✅ You have successfully checked out for the day!")

@bot.message_handler(commands=['leave'])
def leave_command(message):
    bot.reply_to(message, "📅 Please specify the day you want to request leave for.")

@bot.message_handler(commands=['leaderboard'])
def leaderboard_command(message):
    bot.reply_to(message, "🏆 Here is the current team leaderboard (feature under development).")

@bot.message_handler(commands=['taskstatus'])
def taskstatus_command(message):
    bot.reply_to(message, "🔄 Update or view task progress (feature under development).")

@bot.message_handler(commands=['contact'])
def contact_command(message):
    bot.reply_to(message, "📞 Please reach out to the admin team at admin@persistventures.com.")

# Echo Other Messages
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "I'm here to assist! Use /help to see available commands.")

# Reminder Functions
def send_reminder():
    chat_id = '8168610115'  # Replace with the appropriate chat ID
    bot.send_message(chat_id, "⏰ It's 9 AM! Don't forget to check in.")

def send_checkout_reminder():
    chat_id = '8168610115'  # Replace with the appropriate chat ID
    bot.send_message(chat_id, "⏰ It's 5 PM! Don't forget to check out.")

# Schedule Reminders
schedule.every().day.at("09:00").do(send_reminder)
schedule.every().day.at("17:00").do(send_checkout_reminder)

# Background Scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# Start Polling with Status Messages
if __name__ == "__main__":
    try:
        print("Bot is starting...")
        bot.polling()
    except KeyboardInterrupt:
        print("Bot has stopped.")
