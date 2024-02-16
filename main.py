from scrapers.scraper import TeleScraper
from rewriter.rewrite_gpt import GptRewriter
from telethon.sync import TelegramClient
from send_message import SendData
from db.sqllite_main import SQLite

def main():
    scraper = TeleScraper("https://t.me/vgtimes")
    scraper.scraper_text()
    print("[MAIN] Парсинг постов выполнен. Начинаю отправку в бд...")
        
    db = SQLite("db\\02.02.db")
    db.create_table_if_not("scrape")
    
    print(f'{len(scraper.text_posts)} постов в бд')
    for id, post in enumerate(scraper.text_posts):
        db.insert(table="scrape", id=id, post=post)
    print('[MAIN] БД успешно обновлена')
    
    db.take_all("scrape")
    db.create_table_if_not("rewrite")
    gpt = GptRewriter(db.rows)
    print('[MAIN] Начинаю рерайт')
    print(f'{len(db.rows)} постов для рерайта')

    gpt.rewrite()
    for el in gpt.output:
        db.insert(table="rewrite", id=id, post=el)
    
    print('[MAIN] Рерайт выполнен, бд обновлена')
    db.take_all("rewrite")
    
    print('[MAIN] Перехожу к отправке в телеграм')

    data = [text for id, text in db.rows]
    scraper2 = TeleScraper("https://t.me/vgtimes")
    SendData.send_data(scraper2.client, data, 'https://t.me/pon4ik_channel')

        
if __name__ == "__main__":
    main()
