from typing import List, Optional

from maxapi import Bot
from maxapi.enums import TextFormat
from maxapi.types import InputMedia

from .sender import Sender


class MaxSender(Sender):
    def __init__(self, token: str = None, chat_id: int = None):
        self.bot = Bot(token)
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

        await super().send_article(
            title=title,
            text=text,
            photos=photos,
            videos=videos
        )

        self.result = None
        processed_title = f"<b>{title}</b>\n\n" if title else ""
        article = processed_title + text

        is_long_read = len(article) > 4000
        text_chunks = (
            self._split_into_chunks(article, 4000)
            if is_long_read
            else [article]
        )

        attachments = []

        try:
            if photos:
                attachments.extend(
                    InputMedia(path=photo)
                    for photo in photos
                )

            if videos:
                attachments.extend(
                    InputMedia(path=video)
                    for video in videos
                )

            msg = await self.bot.send_message(
                chat_id=self.chat_id,
                text=text_chunks[0],
                attachments=attachments or None,
                format=TextFormat.HTML
            )

            if is_long_read:
                for chunk in text_chunks[1:]:
                    await self.bot.send_message(
                        chat_id=self.chat_id,
                        text=chunk,
                        format=TextFormat.HTML
                    )

            self.result = msg.message.url if msg.message.url is not None \
                else 'Проблема получения ссылки сообщения в MAX: возможно приватный канал или ЛС'

        except Exception as e:
            self.result = f"Проблема отправки статьи в MAX: {e}"
        finally:
            await self.bot.close_session()

    async def repost(self, link: str = None):
        """
        Currently do nothing
        :param link: Link to message
        """
        pass

    def _split_into_chunks(self, text: str, chunk_size: int = 4000) -> list:
        """
        Splits input text into semantically meaningful chunks of specified maximum size.
        :param text: Input string to be split into chunks.
        :param chunk_size: Maximum character length of each chunk (default: 4000).
        :return: List of text chunks
        """
        return super()._split_into_chunks(
            text=text,
            chunk_size=chunk_size
        )