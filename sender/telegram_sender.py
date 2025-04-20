import re
from math import ceil
from typing import Optional, List

from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from sender.sender import Sender


def _split_into_chunks(text: str, chunk_size:int=4096) -> list:
    """
    Splits input text into semantically meaningful chunks of specified maximum size.
    :param text: Input string to be split into chunks.
    :param chunk_size: Maximum character length of each chunk (default: 4096).
    :return: List of text chunks
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)

    blocks = []
    current_block = ''

    for sentence in sentences:
        if len(current_block) + len(sentence) + 1 <= chunk_size:
            if sentence + '\n\n' in text:
                current_block += sentence + '\n\n'
            elif sentence + '\n' in text:
                current_block += sentence + '\n'
            else:
                current_block += sentence + ' '
        else:
            blocks.append(current_block.strip())
            if sentence + '\n\n' in text:
                current_block = sentence + '\n\n'
            elif sentence + '\n' in text:
                current_block = sentence + '\n'
            else:
                current_block = sentence + ' '

    if current_block:
        blocks.append(current_block.strip())

    return blocks


class TelegramSender(Sender):
    def __init__(self, token=None, chat_id=None, group_name=None):
        self.token = token
        self.bot = Bot(token=token)
        self.chat_id = '-' + chat_id
        self.group_name = group_name
        self.result = ''
        self.links = None


    async def send_article(
            self,
            title: str = '',
            text: str = '',
            photos: Optional[List[str]] = None,
            videos: Optional[List[str]] = None,
            delayed_post_date: Optional[int] = None,
            get_links: bool = False,
            return_links: bool = False
    ) -> None:
        """
        Publishes message or multiple messages in Telegram
        :param title: Article title
        :param text: Article text
        :param photos: List of paths to photos
        :param videos: List of video paths
        :param delayed_post_date: Not used
        :param get_links: Not used
        :param return_links: Not used
        :return: Publish result or error log
        """
        await super().send_article(title=title, text=text, photos=photos, videos=videos)
        self.result = ''
        self.links = {
            'photos': [],
            'videos': []
        }

        processed_title = f'<b>{title}</b>\n\n' if title else ''
        article = processed_title + text if title else text

        # Telegram restriction
        is_caption_text = True if len(article) <= 1024 else False
        is_long_read = True if not is_caption_text and len(article) > 4096 else False

        caption = article if is_caption_text is True else None

        media_groups = [MediaGroupBuilder(caption=caption)]
        # If media files more than 10, split them to several groups
        if len(photos) + len(videos) > 10:
            files_count = len(photos) + len(videos) - 10
            chunk_count = ceil(files_count / 10)
            [media_groups.append(MediaGroupBuilder()) for _ in range(chunk_count)]

        files_count = 0
        current_group = 0
        if videos:
            files_count, curr_group = self._add_videos(videos, media_groups, files_count, current_group,
                                                       get_links=get_links)
        if photos:
            self._add_photos(photos, media_groups, files_count, current_group, get_links=get_links)

        try:
            # If send just a media group, message_id accessible in msg[0].message_id, otherwise msg.message_id
            msg = None
            msg_id = None
            if photos or videos:
                for group in media_groups:
                    # If small text and have media (media with caption)
                    msg = await self.bot.send_media_group(self.chat_id, media=group.build())
                    if return_links:
                        new_photo_links, new_video_links = await self._get_links(msg)
                        self.links['photos'] += new_photo_links
                        self.links['videos'] += new_video_links
                    if group.caption:
                        msg_id = msg[0].message_id
                if not (is_caption_text or is_long_read):
                    # If the text is longer than 1024 chars, send them separately
                    msg = await self.bot.send_message(self.chat_id, article, parse_mode='HTML')
            elif (is_caption_text or not is_long_read) and not (photos or videos):
                # Just sends text
                msg = await self.bot.send_message(self.chat_id, article, parse_mode='HTML')
            if is_long_read:
                # If article bigger then 4096 chars (or value of chunk_size), separate them to several messages
                articles = _split_into_chunks(text, chunk_size=4000)
                articles[0] = processed_title + articles[0]
                msg = await self.bot.send_message(self.chat_id, articles[0], parse_mode='HTML')
                msg_id, previous_message_id = [msg.message_id] * 2  # The same values for both variables
                for article in articles[1:]:
                    msg = await self.bot.send_message(self.chat_id, article,
                                                      reply_to_message_id=previous_message_id,
                                                      parse_mode='HTML')
                    previous_message_id = msg.message_id

            if msg_id is None:
                msg_id = msg.message_id

            self.result += f'https://t.me/{self.group_name}/{msg_id}'
        except Exception as e:
            self.result += f'Проблема отправки статьи в Telegram: {e}'
            self.links = None
        finally:
            await self.bot.session.close()
            return self.links if return_links else None

    def _add_photos(
            self,
            photos: list,
            media_groups: list,
            files_count: int = 0,
            curr_group: int = 0,
            get_links: bool = False
    ) -> None:
        """
        Uploads photos to Telegram and categorizes them into MediaGroups
        :param photos: List of paths to photos
        :param media_groups: List of MediaGroup
        :param files_count: Index of last uploaded media in current MediaGroup in media_groups
        :param curr_group: Index of current MediaGroup in media_groups
        :param get_links: Not used
        """
        for photo in photos:
            try:
                file = photo if get_links else FSInputFile(photo)
                media_groups[curr_group].add_photo(file, parse_mode='HTML')
                files_count += 1
                if files_count == 10:
                    files_count = 0
                    curr_group += 1
            except Exception as e:
                self.result += f"Photo upload error {photo}: {e}\n"

    def _add_videos(
            self,
            videos: list,
            media_groups: list,
            files_count: int = 0,
            curr_group: int = 0,
            get_links: bool = False
    ) -> tuple:
        """
        Uploads videos to Telegram and categorizes them into MediaGroups
        :param videos: List of paths to videos
        :param media_groups: List of MediaGroup
        :param files_count: Index of last uploaded media in current MediaGroup in media_groups
        :param curr_group: Index of current MediaGroup in media_groups
        :param get_links: Not used
        :return: Tuple of updated files_count and curr_group
        """
        for video in videos:
            try:
                file = video if get_links else FSInputFile(video)
                media_groups[curr_group].add_video(file, parse_mode='HTML', supports_streaming=True)
                files_count += 1
                if files_count == 10:
                    files_count = 0
                    curr_group += 1
            except Exception as e:
                self.result += f"Video upload error {video}: {e}\n"

        return files_count, curr_group

    async def _get_links(self, message) -> tuple:
        """
        Extracts links to photos and videos from message
        :param message: aiogram.types.message.Message object
        :return: Tuple of lists of photo links and video links
        """
        photos = []
        videos = []

        for media in message:
            if media.photo:
                photo = await self.bot.get_file(media.photo[-1].file_id)
                link = f'https://api.telegram.org/file/bot{self.token}/{photo.file_path}'
                photos.append(link)
            elif media.video:
                video = await self.bot.get_file(media.video.file_id)
                link = f'https://api.telegram.org/file/bot{self.token}/{video.file_path}'
                videos.append(link)

        return photos, videos