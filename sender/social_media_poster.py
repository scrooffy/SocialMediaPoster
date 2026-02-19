import os
import json

import aiohttp
import asyncio

from .vk_sender import VkSender
from .telegram_sender import TelegramSender
from .ok_sender import OkSender
from .max_sender import MaxSender


class SocialMediaPoster:
    def __init__(
            self, telegram: bool = False, vk: bool = False, ok: bool = False, max_msgr: bool = False,
            settings: dict[str, dict[str, str]] = None
    ):
        self.settings = settings
        self.tg = None
        self.vk = None
        self.ok = None
        self.max_msgr = None

        if telegram and 'telegram' in self.settings:
            self.tg = TelegramSender(
                token=self.settings['telegram']['bot_token'],
                chat_id=self.settings['telegram']['chat_id'],
                group_name=self.settings['telegram']['group_name']
            )
        if vk and 'vk' in self.settings:
            self.vk = VkSender(
                token=self.settings['vk']['token'],
                group_id=self.settings['vk']['group_id']
            )
        if ok and 'ok' in self.settings:
            self.ok = OkSender(
                access_token=self.settings['ok']['access_token'],
                application_key=self.settings['ok']['application_key'],
                application_secret_key=self.settings['ok']['application_secret_key'],
                group_id=self.settings['ok']['group_id']
            )
        if max_msgr and 'max' in self.settings:
            self.max_msgr = MaxSender(
                token=self.settings['max']['token'],
                chat_id=self.settings['max']['chat_id']
            )

    async def send_article(
            self, telegram: bool = False, vk: bool = False, ok: bool = False, max_msgr: bool = False,
            title: str = None, text: str = None, files: list[str] = None, date: int = None
    ) -> None:
        """
        Sends article to social networks
        :param telegram: Send to Telegram flag
        :param vk: Send to VK flag
        :param ok: Send to Odnoklassniki flag
        :param max_msgr: Send to MAX flag
        :param title: Title of article (optional)
        :param text: Article body
        :param files: List of paths to media files (videos and photos) (optional)
        :param date: Time when article will become visible (Unix timestamp format) (optional)
        """
        send_to = []
        gathering_list = []

        if vk and self.vk:
            send_to.append(self.vk.send_article)
        if telegram and self.tg:
            send_to.append(self.tg.send_article)
        if ok and self.ok:
            send_to.append(self.ok.send_article)
        if max_msgr and self.max_msgr:
            send_to.append(self.max_msgr.send_article)

        photos, videos = self.separate_files(files) if files else (None, None)

        for social_media in send_to:
            gathering_list.append(
                social_media(text=text, title=title, photos=photos, videos=videos, delayed_post_date=date)
            )

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*gathering_list)

        await session.close()

    async def do_repost(self, vk_link: str = None, ok_link: str = None) -> None:
        """
        Sends a request to repost posts from these links
        :param vk_link: Link from VK like 'https://vk.com/wall-111_222'
        :param ok_link: Link from Odnoklassniki like 'https://ok.ru/group/111/topic/222':
        """
        repost_to = []
        gathering_list = []

        if vk_link and self.vk:
            repost_to.append((self.vk.repost, vk_link))
        if ok_link and self.ok:
            repost_to.append((self.ok.repost, ok_link))

        for social_media, link in repost_to:
            gathering_list.append(social_media(link=link))

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*gathering_list)

        await session.close()

    def separate_files(self, files: list = None) -> tuple:
        """
        Splits the list of files to images and videos separately
        :param files: List of files paths
        :return: Tuple with separated lists of photos and videos
        """

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

    # await a.send_article(telegram=False, vk=False, ok=False, max_msgr=True, text='test text', title='test title')
    # await a.do_repost(ok_link='https://ok.ru/group/123/topic/456')


if __name__ == '__main__':
    asyncio.run(main())
