class Order:

    def __init__(self, chatId):
        self.chatId = chatId
        self.restaurant = None
        self.category = None
        self.dish = None
        self.volume = None

    def print(self):
        print('chatId: ', self.chatId)
        print('restaurant: ', self.restaurant)
        print('category: ', self.category)
        print('dish: ', self.dish)
        print('volume: ', self.volume)