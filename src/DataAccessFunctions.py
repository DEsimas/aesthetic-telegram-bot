import json

def getUserByTelegramChatId(telegramChatId):
    file = open('./src/data/users.json', encoding='utf8')
    users = json.load(file)
    for user in users:
        if user['telegramChatId'] == telegramChatId:
            return user
    return None

def getUsers():
    file = open('./src/data/users.json', encoding='utf-8')
    return json.load(file)

def saveUser(name, surname, bat, office, telegramChatId):
    user = {
        'name': surname + ' ' + name + ' ' + bat,
        'office': office,
        'telegramChatId': telegramChatId
    }
    users = getUsers()
    users.append(user)
    usersJSON = json.dumps(users, indent = 4, ensure_ascii=False)
    file = open('./src/data/users.json', 'w', encoding='utf-8')
    file.write(usersJSON)

def getOffices():
    return ['Авиамоторная', 'Октябрьское Поле']