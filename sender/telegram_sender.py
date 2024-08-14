import re
from math import ceil
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from sender.sender import Sender


def split_into_chunks(text: str, chunk_size=4096) -> list:
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
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.group_name = group_name
        self.result = ''

    async def send_article(self, title='', text='', photos=None, videos=None) -> str:
        await super().send_article(title=title, text=text, photos=photos, videos=videos)
        self.result = ''

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
            [media_groups.append(MediaGroupBuilder()) for i in range(chunk_count)]

        files_count = 0
        current_group = 0
        if videos:
            files_count, curr_group = self.add_videos(videos, media_groups, files_count, current_group)
        if photos:
            self.add_photos(photos, media_groups, files_count, current_group)

        try:
            # If send just a media group, message_id accessible in msg[0].message_id, otherwise msg.message_id
            msg_id = None
            if photos or videos:
                for group in media_groups:
                    msg = await self.bot.send_media_group(self.chat_id, media=group.build())
                    msg_id = msg[0].message_id
                if not (is_caption_text or is_long_read):
                    msg = await self.bot.send_message(self.chat_id, article, parse_mode='HTML')
                    msg_id = msg.message_id
            elif (is_caption_text or not is_long_read) and not (photos or videos):
                msg = await self.bot.send_message(self.chat_id, article, parse_mode='HTML')
                msg_id = msg.message_id
            if is_long_read:
                articles = split_into_chunks(text, chunk_size=3500)
                articles[0] = processed_title + articles[0]
                msg = await self.bot.send_message(self.chat_id, articles[0], parse_mode='HTML')
                msg_id, previous_message_id = [msg.message_id] * 2  # The same values for both variables
                for article in articles[1:]:
                    msg = await self.bot.send_message(self.chat_id, article,
                                                      reply_to_message_id=previous_message_id,
                                                      parse_mode='HTML')
                    previous_message_id = msg.message_id

            self.result += f'https://t.me/{self.group_name}/{msg_id}'
        except Exception as e:
            self.result += f'Проблема отправки статьи в Telegram: {e}'
        finally:
            await self.bot.session.close()
            return self.result

    def add_photos(self, photos: list, media_groups: list, files_count: int, curr_group: int) -> None:
        for photo in photos:
            try:
                media_groups[curr_group].add_photo(FSInputFile(photo), parse_mode='HTML')
                files_count += 1
                if files_count == 10:
                    files_count = 0
                    curr_group += 1
            except Exception as e:
                self.result += f"Ошибка отправки фото {photo}: {e}\n"

    def add_videos(self, videos: list, media_groups: list, files_count: int, curr_group: int) -> tuple:
        for video in videos:
            try:
                media_groups[curr_group].add_video(FSInputFile(video), parse_mode='HTML', supports_streaming=True)
                files_count += 1
                if files_count == 10:
                    files_count = 0
                    curr_group += 1
            except Exception as e:
                self.result += f"Ошибка отправки видео {video}: {e}\n"

        return files_count, curr_group
