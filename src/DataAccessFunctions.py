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
    print(name, surname, bat, office, telegramChatId)
    user = {
        'name': surname + ' ' + name + ' ' + bat,
        'office': office,
        'telegramChatId': telegramChatId,
        'role': 'user'
    }
    users = getUsers()
    users.append(user)
    usersJSON = json.dumps(users, indent = 4, ensure_ascii=False)
    file = open('./src/data/users.json', 'w', encoding='utf-8')
    file.write(usersJSON)

def getOffices():
    return ['Авиамоторная', 'Октябрьское Поле']

def getRestaurants():
    file = open('./src/data/menu.json', encoding='utf8')
    restaurants = json.load(file)
    elements = []
    for r in restaurants:
        elements.append(r['name'])
    return elements

def getCategories(restaurant):
    file = open('./src/data/menu.json', encoding='utf8')
    restaurants = json.load(file)
    for r in restaurants:
        if r['name'] == restaurant:
            elements = []
            for c in r['categories']:
                elements.append(c['name'])
            return elements
    return None

def getDishes(restaurant, category):
    file = open('./src/data/menu.json', encoding='utf8')
    restaurants = json.load(file)
    for r in restaurants:
        if r['name'] == restaurant:
            elements = []
            for c in r['categories']:
                if c['name'] == category:
                    elements = []
                    for d in c['dishes']:
                        elements.append(d['name'] + ".........." + str(d['price']))
                    return elements
        return None
    return None

def getUsersByOffice(office):
    file = open('./src/data/users.json', encoding='utf8')
    users = json.load(file)
    elements = []
    for u in users:
        if u['office'] == office and u['role'] == 'user':
            elements.append(u)
    return elements

def getCourierByOffice(office):
    file = open('./src/data/users.json', encoding='utf8')
    users = json.load(file)
    for user in users:
        if user['role'] == 'courier' and user['office'] == office:
            return user
    return None

def getPaymentByOffice(office):
    return getCourierByOffice(office)['payment']

def addOrder(office, chatId, order):
    file = open('./src/data/orders.json', encoding='utf8')
    offices = json.load(file)
    users = offices[office]
    users[chatId] = {
        "validated": False,
        "order": order
    }
    officesJSON = json.dumps(offices, indent = 4, ensure_ascii=False)
    file = open('./src/data/orders.json', 'w', encoding='utf8')
    file.write(officesJSON)

def validateOrder(office, chatId):
    file = open('./src/data/orders.json', encoding='utf8')
    offices = json.load(file)
    users = offices[office]
    users[chatId] = {
        "validated": True,
        "order": users[str(chatId)]['order']
    }
    officesJSON = json.dumps(offices, indent = 4, ensure_ascii=False)
    file = open('./src/data/orders.json', 'w', encoding='utf8')
    file.write(officesJSON)

def getOrders(office):
    file = open('./src/data/orders.json', encoding='utf8')
    offices = json.load(file)
    orders = offices[office]
    msg = ''
    for id in orders:
        order = orders[id]
        if order['validated']:
            msg += (getUserByTelegramChatId(int(id))['name'] + ':\n')
            for o in order['order']:
                msg += ('   ' + o['restaurant'] + ' - ' + o['category'] + ' - ' + o['dish'] + '\n')
            msg += '\n'
    if len(msg) == 0:
        return 'Заказов нет'
    return msg

def getOrder(office, chatId):
    file = open('./src/data/orders.json', encoding='utf8')
    offices = json.load(file)
    office = offices[office]
    return office[str(chatId)]

def clearOrders(office):
    file = open('./src/data/orders.json', encoding='utf8')
    offices = json.load(file)
    offices[office] = {}
    officesJSON = json.dumps(offices, indent = 4, ensure_ascii=False)
    file = open('./src/data/orders.json', 'w', encoding='utf8')
    file.write(officesJSON)