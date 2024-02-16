from login.tg import LoginTg
import time

class SendData(LoginTg):
    def __init__(self, media=[], text:list=[], channel:str='', sleep:int=1) -> None:
        self.text = text
        self.media = media
        self.channel = channel
        self.sleep = sleep
    
    
    def __sleeping(self):
        time.sleep(self.sleep)
    
    
    @staticmethod
    async def __send_dataaaa_async(client, text='Привет, это проверка работоспособности', channel:str='https://t.me/pon4ik_channel'): #self
        print('[SMess] Начинается отправка сообщений')
        if type(text) == str:
            await client.send_message(channel, text)
        elif type(text) == list:
            for mes in text:
                await client.send_message(channel, mes)
                time.sleep(2)
            
        
        if channel == 'https://t.me/pon4ik_channel':
            print('[SMess|TEST] Сообщение или несколько сообщений в тестовый канала отправлено')
            
            
    @staticmethod
    def send_data(client, text='Привет, это проверка работоспособности', channel:str='https://t.me/pon4ik_channel'): #self
        print('[SMess] Начинается отправка сообщений')
        if type(text) == str:
            client.send_message(channel, text)
        else: 
            for mes in text:
                client.send_message(channel, mes)
                time.sleep(1)
        
        if channel == 'https://t.me/pon4ik_channel':
            print('[SMess|TEST] Сообщение или несколько сообщений в тестовый канала отправлено')
        