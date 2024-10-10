import os
import json
import aiohttp
import asyncio
from sender.vk_sender import VkSender
from sender.telegram_sender import TelegramSender
from sender.ok_sender import OkSender


class SocialMediaPoster:
    def __init__(self, telegram=True, vk=True, ok= True, settings=None):
        self.title = None
        self.text = None
        self.files = []
        self.photos = []
        self.videos = []
        self.delayed_post_date = None
        self.settings = settings

        if telegram:
            self.tg = TelegramSender(
                token=self.settings['telegram']['bot_token'],
                chat_id=self.settings['telegram']['chat_id'],
                group_name=self.settings['telegram']['group_name']
            )
        if vk:
            self.vk = VkSender(
                token=self.settings['vk']['token'],
                group_id=self.settings['vk']['group_id']
            )
        if ok:
            self.ok = OkSender(
                access_token=self.settings['ok']['access_token'],
                application_key=self.settings['ok']['application_key'],
                application_secret_key=self.settings['ok']['application_secret_key'],
                group_id=self.settings['ok']['group_id']
            )

    async def send_article(self, telegram=True, vk=True, ok=True) -> None:
        send_to = []
        gathering_list = []

        if hasattr(self, 'vk'):
            send_to.append((vk, self.vk.send_article))
        if hasattr(self, 'tg'):
            send_to.append((telegram, self.tg.send_article))
        if hasattr(self, 'ok'):
            send_to.append((ok, self.ok.send_article))

        if self.files:
            self.separate_files()

        for send, social_media in send_to:
            if send:
                gathering_list.append(
                    social_media(text=self.text, title=self.title, photos=self.photos, videos=self.videos,
                                 delayed_post_date=self.delayed_post_date))

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*gathering_list)

        await session.close()

    def separate_files(self) -> None:
        pic_extensions = ('jpg', 'jpeg', 'png', 'webp')
        vid_extensions = ('mp4', '3gp', 'avi', 'mov')

        for file in self.files:
            filename, file_extension = os.path.splitext(file)

            if file_extension.lower().endswith(pic_extensions):
                self.photos.append(file)
            elif file_extension.lower().endswith(vid_extensions):
                self.videos.append(file)

    def clear_files(self) -> None:
        self.files.clear()
        self.photos.clear()
        self.videos.clear()


async def main():
    with open('../settings/settings_test.json') as f:
        smp_settings = json.load(f)
    a = SocialMediaPoster(settings=smp_settings)
    a.text = 'test text'
    a.title = 'test title'

    await a.send_article(telegram=False, vk=True, ok=False)


if __name__ == '__main__':
    asyncio.run(main())
