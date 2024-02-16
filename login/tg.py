from telethon.sync import TelegramClient
from config import sad_manners

class LoginTg():
    def __init__(self):
        self.client = TelegramClient(sad_manners.username, sad_manners.api_id, sad_manners.api_hash)
    #     self.username = sad_manners.username
    #     self.api_hash = sad_manners.api_hash
    #     self.api_id = sad_manners.api_id
    #     self.phone = sad_manners.phone
    @staticmethod
    def login():
        return TelegramClient(sad_manners.username, sad_manners.api_id, sad_manners.api_hash)