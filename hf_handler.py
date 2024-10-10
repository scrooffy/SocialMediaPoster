import json
import requests
from huggingface_hub import InferenceClient, configure_http_backend


def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session


class HfHandler:
    def __init__(self, settings):
        configure_http_backend(backend_factory=backend_factory)
        self.client = InferenceClient(api_key=settings['hf']['token'])
        self.model = "meta-llama/Llama-3.2-3B-Instruct"
        self.temp = 0.5
        self.max_tokens = 1024
        self.top_p = 0.7

    def add_emojis_and_tags(self, article: str):
        messages = [
            {
                "role": "system",
                "content": "Добавь в данный текст смайлики так, чтобы он стал более привлекателен \
                в социальных сетях и добавь хэштеги. Смайлики ставь перед началом предложения. \
                Избегай использования смайликов, если это может изменить смысл сообщения или показаться неуместным."
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


if __name__ == '__main__':
    with open('settings/settings.json') as f:
        smp_settings = json.load(f)

    hr_inf = HfHandler(smp_settings)
    text = "sample text"
    message = hr_inf.add_emojis_and_tags(text)
    print(message)