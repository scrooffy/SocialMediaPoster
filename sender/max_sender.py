from typing import List, Dict, Any, Optional
import asyncio

from aiohttp import ClientSession
from aiomax import Bot

from .sender import Sender

class MaxSender(Sender):
    def __init__(self, token: str = None, chat_id: str = None):
        self.bot = Bot(access_token=token)
        self.chat_id = chat_id
        self.result = None

    async def send_article(
            self,
            title: str = '',
            text: str = '',
            photos: Optional[List[str]] = None,
            videos: Optional[List[str]] = None,
            delayed_post_date: Optional[int] = None
    ) -> None:
        """
       Publishes article to MAX
       :param title: Article title
       :param text: Article text
       :param photos: List of paths to photos
       :param videos: List of video paths
       :param delayed_post_date: Unix timestamp for delayed publication (not used)
       """
        await super().send_article(title=title, text=text, photos=photos, videos=videos)

        self.result = None
        text_chunks = []

        processed_title = f'<b>{title}</b>\n\n' if title else ''
        article = processed_title + text if title else text
        if is_long_read:= len(article) > 4000:
            text_chunks = self._split_into_chunks(article, 4000)

        attachments = [] if photos or videos else None

        async with ClientSession() as session:
            self.bot.session = session
            try:
                if videos:
                    attachments += await self._add_videos(videos)
                if photos:
                    attachments += await self._add_photos(photos)

                msg_text = text_chunks[0] if is_long_read else article
                msg = await self.bot.send_message(
                    text=msg_text,
                    chat_id=self.chat_id,
                    format='html',
                    attachments=attachments
                )
                if is_long_read:
                    for chunk in text_chunks[1:]:
                        await self.bot.send_message(
                            text=chunk,
                            chat_id=self.chat_id,
                            format='html'
                        )

                self.result = msg.url if msg.url is not None else ('Проблема получения ссылки сообщения в MAX: '
                                                       'возможно приватный канал или ЛС')
            except Exception as e:
                self.result = f'Проблема отправки статьи в MAX: {e}'

        self.bot.session = None

    async def repost(self, link: str = None):
        """
        Currently do nothing
        :param link: Link to message
        """
        pass

    async def _add_photos(self, photos_paths: List[str] = None, max_concurrent: int = 5) -> List[Dict[str, Any]]:
        """
        Uploads photos to MAX
        :param photos_paths: List of paths to photos
        :param max_concurrent: Number of simultaneous uploads
        :return: List of successfully uploaded photos
        """

        if not photos_paths:
            return []

        semaphore = asyncio.Semaphore(max_concurrent)

        async def upload_with_limit(path: str):
            async with semaphore:
                return await self.bot.upload_image(path)

        tasks = [upload_with_limit(photo) for photo in photos_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        photo_attachments = []
        for result in results:
            if isinstance(result, Exception):
                self.result += f'Ошибка загрузки фото в MAX: {result}'
                continue
            photo_attachments.append(result)

        return photo_attachments

    async def _add_videos(self, video_paths: List[str] = None, max_concurrent: int = 5) -> List[Dict[str, Any]]:
        """
        Uploads videos to MAX
        :param video_paths: List of paths to videos
        :param max_concurrent: Number of simultaneous uploads
        :return: List of successfully uploaded videos
        """

        if not video_paths:
            return []

        semaphore = asyncio.Semaphore(max_concurrent)

        async def upload_with_limit(path: str):
            async with semaphore:
                return await self.bot.upload_video(path)

        tasks = [upload_with_limit(video) for video in video_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        video_attachments = []
        for result in results:
            if isinstance(result, Exception):
                self.result += f'Ошибка загрузки видео в MAX: {result}'
                continue
            video_attachments.append(result)

        return video_attachments

    def _split_into_chunks(self, text: str, chunk_size: int = 4000) -> list:
        """
        Splits input text into semantically meaningful chunks of specified maximum size.
        :param text: Input string to be split into chunks.
        :param chunk_size: Maximum character length of each chunk (default: 4000).
        :return: List of text chunks
        """
        return super()._split_into_chunks(text=text, chunk_size=chunk_size)