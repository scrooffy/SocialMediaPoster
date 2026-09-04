import os
import json
import mimetypes

import aiohttp
import asyncio

from .vk_sender import VkSender
from .telegram_sender import TelegramSender
from .ok_sender import OkSender
from .max_sender import MaxSender


class FileValidationError(ValueError):
    """Raised when attached media files fail validation before sending."""


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

        validation_errors = self._validate_media(photos, videos)
        if validation_errors:
            raise FileValidationError('\n'.join(validation_errors))

        for social_media in send_to:
            gathering_list.append(
                social_media(text=text, title=title, photos=photos, videos=videos, delayed_post_date=date)
            )

        await asyncio.gather(*gathering_list)

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

        await asyncio.gather(*gathering_list)

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

    @staticmethod
    def _validate_file(file: str, expected_prefix: str) -> tuple[bool, str | None]:
        """
        Checks that the file exists, is readable, non-empty and has a MIME type
        starting with `expected_prefix`.
        :param file: Path to the file
        :param expected_prefix: Expected MIME prefix, e.g. 'image/' or 'video/'
        :return: (is_valid, error_message_or_None)
        """
        if not os.path.isfile(file):
            return False, 'файл не найден'
        if not os.access(file, os.R_OK):
            return False, 'файл недоступен для чтения'
        if os.path.getsize(file) == 0:
            return False, 'файл пустой'
        mime_type, _ = mimetypes.guess_type(file)
        if mime_type is None or not mime_type.startswith(expected_prefix):
            return False, f'некорректный тип файла ({mime_type})'
        return True, None

    @classmethod
    def _validate_photo(cls, photo: str) -> tuple[bool, str | None]:
        return cls._validate_file(photo, 'image/')

    @classmethod
    def _validate_video(cls, video: str) -> tuple[bool, str | None]:
        return cls._validate_file(video, 'video/')

    @classmethod
    def _validate_media(cls, photos: list = None, videos: list = None) -> list[str]:
        """
        Validates all photos and videos, returning collected error messages.
        :param photos: List of photo paths
        :param videos: List of video paths
        :return: List of error messages (one per invalid file)
        """
        errors = []
        for media, validator in ((photos, cls._validate_photo), (videos, cls._validate_video)):
            for file in media or []:
                is_valid, error = validator(file)
                if not is_valid:
                    errors.append(f'Проблема загрузки файла: "{file}": {error}')
        return errors


async def main():
    with open('../settings/settings.json') as f:
        smp_settings = json.load(f)
    a = SocialMediaPoster(settings=smp_settings)

    # await a.send_article(telegram=False, vk=False, ok=False, max_msgr=True, text='test text', title='test title')
    # await a.do_repost(ok_link='https://ok.ru/group/123/topic/456')


if __name__ == '__main__':
    asyncio.run(main())
