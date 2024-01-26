import re
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from sender.sender import Sender


# Not the best implementation but ok
def split_into_chunks(text, chunk_size):
    # find all sentences
    matches = re.finditer(r'(.*?)[\.!?]+', text, re.MULTILINE)
    sentences = []
    for matchNum, match in enumerate(matches, start=1):
        sentences.append(match.group())

    # check abbreviations
    word_abbreviations_pattern = re.compile(r'\s\w[\.!?]+')
    processed_sentences = []
    i = 0
    while i < len(sentences):
        if word_abbreviations_pattern.search(sentences[i]):
            # If the current line matches the regular expression, append it to the next one
            processed_sentences.append(sentences[i] + sentences[i + 1])
            i += 2
        else:
            # If the current line does not match the regular expression, simply add it to the result
            processed_sentences.append(sentences[i])
            i += 1

    chunks = []
    current_chunk = ''
    second_chunk_flag = True
    for sentence in processed_sentences:
        if len(current_chunk + sentence) <= chunk_size:
            current_chunk += sentence
        else:
            if second_chunk_flag:
                chunk_size -= 14    # because additional chunks with title = title + ' (Продолжение)'
                second_chunk_flag = False
            chunks.append(current_chunk)
            current_chunk = sentence

    chunks.append(current_chunk)

    return chunks


class TelegramSender(Sender):
    def __init__(self, token=None, chat_id=None, group_name=None):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.group_name = group_name
        self.result = ''

    async def send_article(self, title='', text='', photos=None, videos=None):
        await super().send_article(title=title, text=text, photos=photos, videos=videos)
        self.result = ''

        processed_title = f'<b>{title}</b>\n\n' if title else ''
        article = processed_title + text if title else text

        # Telegram restriction
        is_caption_text = True if len(article) <= 1024 else False
        is_long_read = True if not is_caption_text and len(article) > 4096 else False

        caption = article if is_caption_text is True else None
        media = MediaGroupBuilder(caption=caption)
        if photos:
            for photo in photos:
                try:
                    media.add_photo(FSInputFile(photo), parse_mode='HTML')
                except Exception as e:
                    self.result += f"Ошибка отправки фото {photo}: {e}\n"
        if videos:
            for video in videos:
                try:
                    media.add_video(FSInputFile(video), parse_mode='HTML')
                except Exception as e:
                    self.result += f"Ошибка отправки видео {video}: {e}\n"

        try:
            # If send just a media group, message_id accessible in msg[0].message_id, otherwise msg.message_id
            msg_id = None
            if photos or videos:
                msg = await self.bot.send_media_group(self.chat_id, media=media.build())
                msg_id = msg[0].message_id
                if not (is_caption_text or is_long_read):
                    msg = await self.bot.send_message(self.chat_id, article, parse_mode='HTML')
                    msg_id = msg.message_id
            elif (is_caption_text or not is_long_read) and not (photos or videos):
                msg = await self.bot.send_message(self.chat_id, article, parse_mode='HTML')
                msg_id = msg.message_id
            if is_long_read:
                articles = split_into_chunks(text, 4096 - len(processed_title))
                articles[0] = processed_title + articles[0]
                articles[1:] = [f'<b>{title}  (Продолжение)</b>\n\n{i}' for i in articles[1:]]

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
