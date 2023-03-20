import re

valid_mail = [ 'gmail', 'hotmail', 'outlook', 'yahoo', 'yandex']

def check_isUsername(username):
    pattern = r"^[a-zA-Z\-]+$"
    return bool(re.match(pattern, username))

def check_isPassword(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))

###def check_isPassword(password):
    upper = 0
    number = 0
    symbol = 0
    for letter in password:
        if letter.isupper():
            upper += 1
        elif letter.isnumeric():
            number += 1
        elif not letter.isalpha():
            symbol += 1
    return upper > 0 and number > 0 and symbol > 0 and len(password) > 7

def check_isEmail(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def check_phone_number(phone_number):
    return bool(re.match('^[+0-9]{10,}$', phone_number))

#def check_isEmail(email):
#    if len(email) == 0:
#        return False
#    isValid = False
#    for i in range(0, len(email) - 1):
#        if (email[i] == '@' and i > 0):
#            for j in range(i, len(email) - 1):
#                if (email[j] == '.' and email[j + 1] == 'c' and email[j + 2] == 'o'and email[j + 3] == 'm' and j > i + 1):
#                    isValid = True
#    return isValid