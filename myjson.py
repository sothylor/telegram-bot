import json

with open('users.json') as f:
    users = json.load(f)

def add_data(chat_id,username, password, email, phone_number):

    new_user = {'chat_id': chat_id, 'username': username, 'password': password, 'email': email, 'phone_number': phone_number}
    users.append(new_user)
 
    with open('users.json', 'w') as f:
        json.dump(users, f )
def update_password(password, user):
    user['password'] = password
    with open('users.json', 'w') as f:
        json.dump(users, f)
def update_whitelist(user):
    user['whitelist'] = True
    with open('users.json', 'w') as f:
        json.dump(users, f)
    