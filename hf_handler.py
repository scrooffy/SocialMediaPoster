import json
import requests
from huggingface_hub import InferenceClient, configure_http_backend
# from huggingface_hub import AsyncInferenceClient

def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session


class HfHandler:
    def __init__(self, settings):
        configure_http_backend(backend_factory=backend_factory)
        self.client = InferenceClient(api_key=settings['token'])
        # self.async_client = AsyncInferenceClient(api_key=settings['token'])
        self.model = settings['model']
        self.system_prompt = settings['system_prompt']
        self.temp = 0.5
        self.max_tokens = 1024
        self.top_p = 0.7

    def add_emojis_and_tags(self, article: str):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": article
            }
        ]

        out = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
            temperature=self.temp,
            max_tokens=self.max_tokens,
            top_p=self.top_p
        )

        return out.choices[0].message['content']

    # Doesn't work
    # async def add_emojis_and_tags_async(self, article: str):
    #     messages = [
    #         {
    #             "role": "system",
    #             "content": self.system_prompt
    #         },
    #         {
    #             "role": "user",
    #             "content": article
    #         }
    #     ]
    #
    #     out = await self.async_client.chat.completions.create(
    #         model=self.model,
    #         messages=messages,
    #         stream=False,
    #         temperature=self.temp,
    #         max_tokens=self.max_tokens,
    #         top_p=self.top_p
    #     )
    #
    #     return out.choices[0].message['content']

if __name__ == '__main__':
    with open('settings/settings.json', encoding='utf_8_sig') as f:
        smp_settings = json.load(f)

    hr_inf = HfHandler(smp_settings['hf'])
    text = "sample text"
    message = hr_inf.add_emojis_and_tags(text)
    print(message)