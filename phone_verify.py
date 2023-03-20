import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint

# Initialize Telegram bot with your bot token
bot = telegram.Bot(token='YOUR_BOT_TOKEN')

# Define a command to start phone verification
def start(update, context):
    # Generate a random 6-digit scode
    code = randint(100000, 999999)
    # Save the code to the user's context
    context.user_data['code'] = code
    # Ask the user to enter their phone number
    update.message.reply_text('Please enter your phone number (in international format):')

# Define a message handler to verify the phone number
def verify_phone(phone_number):
    code = randint(100000, 999999)
    message = f'Your verification code is: {code}'
    bot.send_message(chat_id=phone_number, text=message)
    message.reply_text('Please enter the 6-digit verification code that you received on your phone:')

# Define a message handler to check the verification code
def check_code(update, context):
    # Get the verification code from the message
    user_code = update.message.text
    # Get the verification code from the user's context
    code = context.user_data.get('code')
    if not code:
        update.message.reply_text('Verification code not found. Please use /start command to start verification.')
        return
    # Check if the verification code matches
    if user_code == str(code):
        update.message.reply_text('Phone number verified successfully!')
    else:
        update.message.reply_text('Invalid verification code. Please try again.')

# Set up the Telegram bot with handlers
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.regex('^[+0-9]{10,}$'), verify_phone))
dispatcher.add_handler(MessageHandler(Filters.regex('^[0-9]{6}$'), check_code))

# Start the bot
updater.start_polling()
