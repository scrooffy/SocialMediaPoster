import os
import json
import aiohttp
import asyncio
from sender.vk_sender import VkSender
from sender.telegram_sender import TelegramSender
from sender.ok_sender import OkSender


class SocialMediaPoster:
    def __init__(self):
        self.title = None
        self.text = None
        self.files = []
        self.photos = []
        self.videos = []

        self.settings = self.get_settings('settings/settings.json')

        self.tg = TelegramSender(
            token=self.settings['telegram']['bot_token'],
            chat_id=self.settings['telegram']['chat_id'],
            group_name=self.settings['telegram']['group_name']
        )
        self.vk = VkSender(
            token=self.settings['vk']['token'],
            group_id=self.settings['vk']['group_id']
        )
        self.ok = OkSender(
            access_token=self.settings['ok']['access_token'],
            application_key=self.settings['ok']['application_key'],
            application_secret_key=self.settings['ok']['application_secret_key'],
            group_id=self.settings['ok']['group_id']
        )

        self.ok_results = ''

    def get_settings(self, relative_path):
        absolute_path = os.path.dirname(__file__)
        full_path = os.path.join(absolute_path, relative_path)

        with open(full_path) as f:
            settings = json.load(f)

        return settings

    async def send_article(self, telegram=True, vk=True, ok=True):
        send_to = []

        if self.files:
            self.separate_files()

        if telegram:
            send_to.append(
                self.tg.send_article(text=self.text, title=self.title, photos=self.photos, videos=self.videos)
            )
        if vk:
            send_to.append(
                self.vk.send_article(text=self.text, title=self.title, photos=self.photos, videos=self.videos)
            )
        if ok:
            send_to.append(
                self.ok.send_article(text=self.text, title=self.title, photos=self.photos)
            )

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*send_to)
        await session.close()

    def separate_files(self):
        pic_extensions = ('jpg', 'jpeg', 'png', 'webp')
        vid_extensions = ('mp4', '3gp', 'avi', 'mov')

        for file in self.files:
            filename, file_extension = os.path.splitext(file)

            if file_extension.lower().endswith(pic_extensions):
                self.photos.append(file)
            elif file_extension.lower().endswith(vid_extensions):
                self.videos.append(file)


async def main():
    a = SocialMediaPoster()
    a.text = 'test'
    a.title = 'test'
    # a.videos.append('vid.mp4')
    # a.photos.append('icon256.png')
    # a.photos.append('icon256.png')

    await a.send_article(telegram=True, vk=False, ok=False)


if __name__ == '__main__':
    asyncio.run(main())
