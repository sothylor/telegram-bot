from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import telebot
from myjson import update_whitelist, users, add_data, update_password
from verify import email_verify, send_verify, otp_acceptance
from myapi import Token
from validation import check_isEmail, check_isPassword, check_isUsername, check_phone_number
from init import cat_markup, menu_markup

bot = telebot.TeleBot(Token, parse_mode=None)

cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_markup.row('/cancel')

callback_running = False
use_usernames = False
login_status = False
requirements = False
click_facebook = click_discord = click_instagram = click_twitter = False

@bot.message_handler(commands=['start'])
def begin_init(message) :
    global message_id_login_status
    if (login_status == False):
        bot.send_message(message.chat.id, "Account Status: Log out", reply_markup=ReplyKeyboardRemove())
        bot.send_message(message.chat.id, 'Button options', reply_markup=cat_markup)
    else:
        bot.send_message(message.chat.id, "Account Status: Log in", reply_markup=ReplyKeyboardRemove())
        bot.send_message(message.chat.id, "Choose your options", reply_markup=menu_markup)

def phone_number_count(phone_number):
    count = 0
    for user in users:
        if (user['phone_number'] == phone_number):
            count += 1
    return count

# /start comands

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    global callback_running, login_status, message_id_login_status
    if call.data == '/help' and callback_running :
        bot.send_message(call.message.chat.id, "+ Help: show the help message\n+ Show Menu: type /start to show menu or go to home.\n+ Sign in: use to login to account." + "\n+ Sign Up: use to create the account." + "\n+ Forgot Password: If you forget your password use /start and click Forgot password")
    elif call.data == '/signup' and callback_running == False:
        callback_running = True
        if (call.message.chat.username == None):
            bot.send_message(call.message.chat.id, "Please enter a username using only letters.", parse_mode="HTML", reply_markup=cancel_markup)
            bot.register_next_step_handler(call.message, get_username)
        else:
            bot.send_message(call.message.chat.id, "Your username is " + call.message.chat.username)
            bot.register_next_step_handler(call.message.chat.username, get_username)
    elif call.data == '/signin'and callback_running == False:
        callback_running = True
        bot.send_message(call.message.chat.id, "Please enter your email address or username.",reply_markup=cancel_markup)
        bot.register_next_step_handler(call.message, check_signin)
    elif call.data == '/forgot' and callback_running == False:
        callback_running = True
        bot.send_message(call.message.chat.id, "Please enter your email address to reset your password.",reply_markup=cancel_markup)
        bot.register_next_step_handler(call.message, reset_email)
    elif call.data == 'facebook':
        global click_facebook, facebook_button
        bot.send_message(call.message.chat.id, 'you have enter facebook link')
        click_facebook = True
    elif call.data == 'instagram':
        global click_instagram
        bot.send_message(call.message.chat.id, 'you have enter instagram link')
        click_instagram = True
    elif call.data == 'discord':
        global click_discord
        bot.send_message(call.message.chat.id, 'you have enter discord link')
        click_discord = True
    elif call.data == 'twitter':
        global click_twitter
        bot.send_message(call.message.chat.id, 'you have enter twitter link')
        click_twitter = True
    elif call.data == 'sign_out' and callback_running == False:
        global message_id_login_status
        login_status = False
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id-1, reply_markup=cat_markup)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.edit_message_text(text="Account Status: Log out", chat_id = call.message.chat.id, message_id = call.message.message_id - 2)
    elif call.data == 'whitelist' and callback_running == False and login_status == True:
        callback_running = True
        for user in users:
            if user['chat_id'] == call.message.chat.id:
                if user['whitelist'] == True:
                    bot.send_message(call.message.chat.id, "You already in whitelist")
                    callback_running = False
                else:
                    if (click_twitter and click_discord and click_instagram and click_facebook):
                        bot.send_message(call.message.chat.id, "You have successfully joined whitelist.", reply_markup=ReplyKeyboardMarkup())
                        update_whitelist(user)
                        callback_running = False
                    else:
                        bot.send_message(call.message.chat.id, "Do the all task above and try again.", reply_markup=ReplyKeyboardMarkup())
                        callback_running = False
                break

# /register
def get_username(message):
    global callback_running
    username = message.text
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    if not check_isUsername(username):
        bot.reply_to(message, "Invalid username. Please enter a valid username with only alphabetical characters.\nCanceled, you can use /start again to start",reply_markup=cancel_markup)
        bot.register_next_step_handler(message, get_username)
        return
    if any(user['username'] == username for user in users):
        bot.reply_to(message, "This username is already taken. please try again",reply_markup=cancel_markup)
        bot.register_next_step_handler(message, get_username)
        return
    bot.send_message(message.from_user.id, 'Please enter a password with at least one uppercase letter, symbol, number, and a minimum of 8 characters.',reply_markup=cancel_markup)
    message_id = message.message_id
    bot.register_next_step_handler(message, get_password, username, message_id + 2)

def get_password(message, username, message_id):
    global callback_running
    password = message.text
    chat_id = message.chat.id
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    if not check_isPassword(password):
        bot.send_message(message.chat.id, 'Your password must contain Minimum pf eight characters, at least one uppercase letter, one lowercase letter, one number and one special character',reply_markup=cancel_markup)
        bot.register_next_step_handler(message, get_password, username, message_id)
        return
    bot.send_message(message.chat.id, "Your password: " + "*" * len(message.text))
    bot.send_message(message.from_user.id, "Please enter your email address.",reply_markup=cancel_markup)
    bot.register_next_step_handler(message, get_email, username, password)
    bot.delete_message(chat_id=chat_id, message_id=message_id)

def get_email(message, username, password):
    global callback_runningw
    email = message.text
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    if not check_isEmail(email):
        bot.reply_to(message, "Invalid email address. Please enter a valid email address.",reply_markup=cancel_markup)
        bot.register_next_step_handler(message, get_email, username, password)
        return
    if any(user['email'] == email for user in users):
        bot.reply_to(message, "This email address is already in use. Please use a different email address.",reply_markup=cancel_markup)
        bot.register_next_step_handler(message, get_email, username, password)
        return
    try:
        verify_code = email_verify(email)
        bot.reply_to(message, "A verification code has been sent to your email address. Please enter the code to confirm your email.", reply_markup=cancel_markup)
        bot.register_next_step_handler(message, confirm_verify, username, password, email, verify_code)
    except Exception as e:
        bot.reply_to(message, e + " Unable to send code to the given email address. Please enter a different email address or click cancel to exit registration.")
        bot.register_next_step_handler(message, get_email, username, password)


def confirm_verify(message, username, password, email, verify_code):
    global callback_running
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    if verify_code != message.text:
        bot.reply_to(message, "Incorrect verification code. Please try again.",reply_markup=cancel_markup)
        bot.register_next_step_handler(message, confirm_verify, username, password, email, verify_code)
    else:
        bot.send_message(message.chat.id, "Verification Completed", reply_markup=cancel_markup)
        bot.send_message(message.chat.id, "Please enter your phone number", reply_markup=cancel_markup)
        bot.register_next_step_handler(message, number_verify, username, password, email)
    
def number_verify(message, username, password, email):
    global callback_running
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    phone_number = message.text
    print(phone_number)
    if not (check_phone_number(phone_number)):
        bot.send_message(message.from_user.id, 'Phone number incorrect or wrong format (Ex:+85590262395), please try again.', reply_markup=cancel_markup)
        bot.register_next_step_handler(message, number_verify, username, password, email)
        return
    if phone_number_count(phone_number) > 3:
        bot.reply_to(message, "This phone_number is already use many time. Please use a different phone number.",reply_markup=cancel_markup)
        bot.register_next_step_handler(message, number_verify, username, password, email)
        return
    if (send_verify(phone_number) == "pending"):
        bot.send_message(message.from_user.id, 'Please enter your verification code:', reply_markup=cancel_markup)
        bot.register_next_step_handler(message, get_otp, username, password, email, phone_number)
    else:
        bot.send_message(message.from_user.id, 'Phone number incorrect or wrong format (Ex:+85590262395), please try again.', reply_markup=cancel_markup)
        bot.register_next_step_handler(message, number_verify, username, password, email)
        return
        
def get_otp(message, username, password, email, phone_number):
    global callback_running
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    status = otp_acceptance(phone_number, message.text)
    if (status == 'approved'):
        add_data(message.chat.id,username, password, email, phone_number)
        bot.send_message(message.chat.id, "Registration complete. You can now log in with your account",reply_markup=ReplyKeyboardRemove())
        callback_running = False
    else:
        bot.send_message(message.from_user.id, "Incorrect verification code, Please re-enter your verification code.",reply_markup=cancel_markup)
        bot.register_next_step_handler(message.from_user.id, get_otp, username, password, email, phone_number)
                         
# /signin commands

def check_signin(message):
    global callback_running
    global use_usernames
    username = message.text
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    if (check_isEmail(message.text)):
        if (any(user['email'] == message.text for user in users)):
            use_usernames = False
            bot.send_message(message.from_user.id, "Please enter your password.",reply_markup=cancel_markup)
            message_id = message.message_id
            bot.register_next_step_handler(message, check_password, username, message_id + 2)
    elif any(user['username'] == message.text for user in users):
        use_usernames = True
        bot.send_message(message.from_user.id, "Please enter your password.",reply_markup=cancel_markup)
        message_id = message.message_id
        bot.register_next_step_handler(message, check_password, username, message_id + 2)
    else:
        bot.reply_to(message, "No account found with this username or email.\nProgress canceled, please use /start and register again.",reply_markup=ReplyKeyboardRemove())
        callback_running = False

def check_password(message, username, message_id):
    global callback_running, use_usernames, login_status, message_id_login_status
    chat_id = message.chat.id
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    for user in users:
        if (user['username'] == username or user['email'] == username) and user['password'] == message.text:
            bot.send_message(message.chat.id, "Your password: " + "*" * len(message.text))
            bot.send_message(message.chat.id, f"Welcome, {user['username']}!           ")
            login_status = True
            bot.delete_message(chat_id=chat_id, message_id=message_id)
            callback_running = False
            bot.send_message(message.chat.id, "Account Status: Log in")
            message_id_login_status = message.message_id + 3
            bot.send_message(message.chat.id, "Choose your options", reply_markup=menu_markup)
            return
    bot.reply_to(message, "Incorrect password. Please try again.",reply_markup=cancel_markup)
    bot.register_next_step_handler(message, check_password, username, message_id)

# /reset commands

def reset_email(message):
    global callback_running
    email = message.text
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    if not check_isEmail(email):
        bot.reply_to(message, "Invalid email address, please enter a valid one.",reply_markup=cancel_markup)
        bot.register_next_step_handler(message, reset_email)
        return
    if not any(user['email'] == email for user in users):
        bot.reply_to(message, "The email address is not register, please try again or register a new account.",reply_markup=cancel_markup)
        bot.register_next_step_handler(message, reset_email)
        return
    verify_code = email_verify(email)
    bot.send_message(message.chat.id, "A verification code has been sent to your email. Please enter the code to continue.",reply_markup=cancel_markup)
    bot.register_next_step_handler(message, confirm_email, email, verify_code)

def confirm_email(message, email, verify_code):
    global callback_running
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    if message.text == verify_code:
        bot.reply_to(message, "Correct verification code")
        bot.send_message(message.from_user.id,"Please enter your new password.",reply_markup=cancel_markup)
        message_id = message.message_id
        bot.register_next_step_handler(message, reset_password, email, message_id + 3)
    else:
        bot.reply_to(message, "Incorrect verification code, Please try again.",reply_markup=cancel_markup)
        bot.register_next_step_handler(message, confirm_email, email, verify_code)

def reset_password(message, email,message_id):
    global callback_running
    password = message.text
    chat_id = message.chat.id
    if (message.text == '/cancel'):
        bot.send_message(message.from_user.id, 'Canceled, you can use /start again to start', reply_markup=ReplyKeyboardRemove())
        callback_running = False
        return
    if not (check_isPassword(password)):
        bot.reply_to(message, "Invalid password. Password should contain at least 1 uppercase letter, symbol, number, and be at least 8 characters long.",reply_markup=cancel_markup)
        bot.register_next_step_handler(message, reset_password, email, message_id)
        return
    for user in users:
        if user['email'] == email:
            update_password(password, user)
            bot.send_message(message.chat.id, "Your password: " + "*" * len(password))
            bot.send_message(message.chat.id, "Password successfully updated.", reply_markup=ReplyKeyboardRemove())
            bot.delete_message(chat_id=chat_id, message_id=message_id)
            break
    callback_running = False


# Defualt
@bot.message_handler(func=lambda m: True)
def default(message):
    bot.send_message(message.chat.id, "Please <b>/start</b> to start show bot button", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

bot.polling()