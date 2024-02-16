import asyncio
import time
import g4f


#! проверка работоспособных провайдеров
# print([
#     provider.__name__
#     for provider in g4f.Provider.__providers__
#     if provider.working
# ])

class GptRewriter:
    def __init__(self, prompts='Привет, ты работаешь?'):
        self.prompts = prompts
        self.cnt = 0
        self.conf_prompt = 'Rewrite the following text to make it more sarcastic in russian language:'
        self.output1 = ''
        self.output = []
	
    async def __rewrite_async(self):
        prompts = self.prompts
        if type(prompts) == list:
            for prompt in self.prompts:
                end_prompt = self.conf_prompt + prompt
                response = g4f.ChatCompletion.create_async(
                    # model="gpt-3.5-turbo",
                    model=g4f.models.gpt_4,
                    # provider=g4f.Provider.GeekGpt,
                    provider=g4f.Provider.Bing,
                    messages=[{"role": "user", "content": end_prompt}],
                    # stream=True,
                    # proxy="socks5://user:pass@host:port"
                    proxy="socks5://41070:Gbhy65@176.106.53.179:41070", # Сашина прокся, работает всё безупречно
                    # proxy="socks5://wpujiJaH:2nJAhLMm@188.190.11.106:64087", # не коннектится
                    # timeout=120,
                )
                resp = await asyncio.gather(response)
                self.output.append(resp)
                time.sleep(1)
            print(f'[RE] Рерайт {len(self.output)} элементов выполнен, находится в .output')
            
        elif type(prompts) == str:
            end_prompt = self.conf_prompt + prompts
            response = g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4,
                provider=g4f.Provider.Bing,
                messages=[{"role": "user", "content": end_prompt}],
                proxy="socks5://41070:Gbhy65@176.106.53.179:41070"
            )
            resp = await asyncio.gather(response)
            self.output1 = resp
            print(f'[RE] Рерайт одного элемента выполнен, находится в .output1')
            print(resp)
            
            
    def rewrite(self):
        self.cnt = 1
        prompts = self.prompts
        if type(prompts) == list:
            for prompt in self.prompts:
                print(f'[RE] Рерайт {self.cnt} элемента из {len(self.prompts)}')
                self.cnt += 1
                end_prompt = self.conf_prompt + prompt
                # response = g4f.ChatCompletion.create(
                #     # model="gpt-3.5-turbo",
                #     model=g4f.models.gpt_4,
                #     # provider=g4f.Provider.GeekGpt,
                #     provider=g4f.Provider.Bing,
                #     messages=[{"role": "user", "content": end_prompt}],
                #     # stream=True,
                #     # proxy="socks5://user:pass@host:port"
                #     proxy="socks5://41070:Gbhy65@176.106.53.179:41070", # Сашина прокся, работает всё безупречно
                #     # proxy="socks5://wpujiJaH:2nJAhLMm@188.190.11.106:64087", # не коннектится
                #     # timeout=120,
                # )
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    provider=g4f.Provider.Bing,
                    messages=[{"role": "user", "content": end_prompt}],
                    proxy="socks5://41070:Gbhy65@176.106.53.179:41070",
                    timeout=400,
                )
                self.output.append(response)
                time.sleep(10)
                
            print(f'[RE] Рерайт {len(self.output)} элементов выполнен, находится в .output')
            
        elif type(prompts) == str:
            end_prompt = self.conf_prompt + prompts
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                provider=g4f.Provider.Bing,
                messages=[{"role": "user", "content": end_prompt}],
                proxy="socks5://41070:Gbhy65@176.106.53.179:41070"
            )
            self.output1 = response
            print(f'[RE] Рерайт одного элемента выполнен, находится в .output1')
            # print(response)

# gpt = GptRewriter(['Привет, ты работаешь?', 'Объясни, 1 градус, больше чем 2', 'Какой цвет похож на синий?', 'Ты работаешь?', ' Ты тут есть?', 'Ты настоящий?'])
# gpt.rewrite()