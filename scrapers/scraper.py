# from config import sad_manners
# from telethon.sync import TelegramClient
from db.sqllite_main import SQLite
from login.tg import LoginTg
import time

# api_id = sad_manners.api_id
# api_hash = sad_manners.api_hash
# phone = sad_manners.phone
# username = sad_manners.username

class TeleScraper(LoginTg):
    def __init__(self, parse_url='https://t.me/vgtimes'):
        super().__init__()
        self.parse_url = parse_url
        self.text_posts = []

    def __del__(self):
        self.client.disconnect()
        
    async def scrape_text_async(self, client):
        async for message in client.iter_messages(self.parse_url, limit=100):
            if message.text:
                self.text_posts.append(message.text)
            if len(self.text_posts) == 4:
                print('[SC|Info] Нужное колличество постов получено')
                break
            time.sleep(2)
            
    def scraper(self):
        self.client.connect()
        
        for message in self.client.iter_messages(self.parse_url, limit=100):
            if message.text:
                self.text_posts.append(message.text)
            if len(self.text_posts) == 3:
                print('[SC|Info] Нужное колличество постов получено')
                break
            time.sleep(2)
            
        self.client.disconnect()
    
    


if __name__ == '__main__':
    # scraper = TeleScraper("https://t.me/vgtimes")
    # scraper.scrape_text()
    # print(scraper.text_posts)
    scraper = TeleScraper("https://t.me/vgtimes")
    # #? scraper.client.loop.run_until_complete(scraper.scrape_text_async(scraper.client))
    scraper.scraper()
    print("[MAIN] Парсинг постов выполнен. Начинаю отправку в бд...")
        
    db = SQLite("db\\02.02.db")
    db.create_table("scrape")
    
    print(f'{len(scraper.text_posts)} постов в бд')
    for id, post in enumerate(scraper.text_posts):
        db.insert(table="scrape", id=id, post=post)