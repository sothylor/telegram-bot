from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import telebot
from myjson import users, add_data, update_password
from verify import email_verify, send_verify, otp_acceptance
from myapi import Token
from validation import check_isEmail, check_isPassword, check_isUsername, check_phone_number
bot = telebot.TeleBot(Token, parse_mode=None)

# Global variables
callback_running = False
use_usernames = False
def phone_number_count(phone_number):
    count = 0
    for user in users:
        if (user['phone_number'] == phone_number):
            count += 1
    return count


facebook_button = InlineKeyboardButton(text = '1. Join Facebook Group', url='https://www.facebook.com/groups/your_group')
facebook_button_follow = InlineKeyboardButton('Finished Joined', callback_data='facebook')
instagram_button = InlineKeyboardButton(text = '2. Follow Instagram', url='https://www.instagram.com/your_instagram')
instagram_button_follow = InlineKeyboardButton('Finished Followed', callback_data= 'instagram')
discord_button = InlineKeyboardButton(text = '3. Join Discord Channel', url='https://discord.gg/your_channel')
discord_button_follow = InlineKeyboardButton('Finished Joined', callback_data = 'discord')
twitter_button = InlineKeyboardButton(text = '4. Follow Twitter', url='https://twitter.com/your_twitter')
twitter_button_follow = InlineKeyboardButton('Finished Followed', callback_data = 'twitter')
whitelist_button = InlineKeyboardButton('Join Whitelist', callback_data="whitelist")
help_button = InlineKeyboardButton('Help', callback_data='/help')
sign_in_button = InlineKeyboardButton('Sign In', callback_data='/signin')
sign_up_button = InlineKeyboardButton('Sign Up', callback_data='/signup')
sign_out_button = InlineKeyboardButton('Sign Out', callback_data='sign_out')
forgot_password_button = InlineKeyboardButton('Forgot Password', callback_data='/forgot')

menu_markup = InlineKeyboardMarkup(row_width=2)
menu_markup.add(facebook_button, facebook_button_follow)
menu_markup.add(instagram_button, instagram_button_follow)
menu_markup.add(discord_button, discord_button_follow)
menu_markup.add(twitter_button, twitter_button_follow)
menu_markup.add(whitelist_button)
menu_markup.add(sign_out_button)

cat_markup = InlineKeyboardMarkup(row_width=2)
cat_markup.add(sign_in_button)
cat_markup.add(sign_up_button)
cat_markup.add(forgot_password_button)


