from aiogram import Bot, types
from sender.sender import Sender


class TelegramSender(Sender):
    def __init__(self, token=None, chat_id=None, group_name=None):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.group_name = group_name
        self.result = ''

    async def send_article(self, title='', text='', photos=None, videos=None):
        await super().send_article(title=title, text=text, photos=photos, videos=videos)
        self.result = ''

        if photos is None:
            photos = []
        article = f'<b>{title}</b>\n\n{text}' if title else text
        media = types.MediaGroup()
        if photos:
            for photo in photos:
                try:
                    media.attach_photo(types.InputFile(photo))
                except Exception as e:
                    self.result += f"Ошибка отправки фото {photo}: {e}\n"
        if videos:
            for video in videos:
                try:
                    media.attach_video(types.InputFile(video))
                except Exception as e:
                    self.result += f"Ошибка отправки видео {video}: {e}\n"

        try:
            msg = await self.bot.send_message(self.chat_id, article, reply_markup=None, parse_mode='HTML')
            if photos or videos:
                await self.bot.send_media_group(self.chat_id, media=media)

            self.result += f'https://t.me/{self.group_name}/{msg["message_id"]}'
        except Exception as e:
            self.result += f'Проблема отправки статьи в Telegram: {e}'
        finally:
            s = await self.bot.get_session()
            await s.close()
            return self.result
