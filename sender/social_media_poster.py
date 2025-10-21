import os
import json

import aiohttp
import asyncio

from .vk_sender import VkSender
from .telegram_sender import TelegramSender
from .ok_sender import OkSender


class SocialMediaPoster:
    def __init__(self, telegram=True, vk=True, ok= True, settings=None):
        self.title = None
        self.text = None
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

    async def send_article(
            self, telegram=False, vk=False, ok=False,
            title=None, text=None, files=None, date=None
    ) -> None:
        send_to = []
        gathering_list = []

        if vk:
            send_to.append(self.vk.send_article)
        if telegram:
            send_to.append(self.tg.send_article)
        if ok:
            send_to.append(self.ok.send_article)

        photos, videos = self.separate_files(files) if files else (None, None)

        for social_media in send_to:
            gathering_list.append(
                social_media(text=text, title=title, photos=photos, videos=videos, delayed_post_date=date)
            )

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*gathering_list)

        await session.close()

    async def do_repost(self, vk_link=None, ok_link=None) -> None:
        repost_to = []
        gathering_list = []

        if vk_link:
            repost_to.append((self.vk.repost, vk_link))
        if ok_link:
            repost_to.append((self.ok.repost, ok_link))

        for social_media, link in repost_to:
            gathering_list.append(social_media(link=link))

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*gathering_list)

        await session.close()

    def separate_files(self, files: list = None) -> tuple:
        pic_extensions = ('jpg', 'jpeg', 'png', 'webp')
        vid_extensions = ('mp4', '3gp', 'avi', 'mov')
        photos, videos = [], []

        for file in files:
            filename, file_extension = os.path.splitext(file)

            if file_extension.lower().endswith(pic_extensions):
                photos.append(file)
            elif file_extension.lower().endswith(vid_extensions):
                videos.append(file)

        return photos, videos


async def main():
    with open('../settings/settings.json') as f:
        smp_settings = json.load(f)
    a = SocialMediaPoster(settings=smp_settings)
    a.title = 'test title'
    a.text = 'test text'
    # a.videos.append('path')
    # a.photos.append('path')

    # await a.send_article(telegram=False, vk=True, ok=False)
    # await a.do_repost(vk_link='https://vk.com/wall-asdas')
    # await a.do_repost(ok_link='https://ok.ru/group/123/topic/456')


if __name__ == '__main__':
    asyncio.run(main())
