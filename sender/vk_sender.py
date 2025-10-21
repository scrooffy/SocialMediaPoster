import re
import json
import mimetypes
import asyncio
from math import ceil
import aiohttp
import aiofiles

from .sender import Sender


class VkSender(Sender):
    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.result = None

    async def send_article(
            self, title: str = '', text: str ='',
            photos: list = None, videos: list = None, delayed_post_date: int = None
    ) -> None:
        """
        Sends an article on VK with the specified data
        :param title: Title of article
        :param text: Text of article
        :param photos: List of photo paths
        :param videos: List of video paths
        :param delayed_post_date: Time in Unix timestamp format
        :return: None
        """
        await super().send_article(title=title, text=text, photos=photos, videos=videos)
        if videos is None:
            videos = []
        if photos is None:
            photos = []
        self.result = ''

        article = f'{title}\n\n{text}' if title else text
        attachments = []

        async with aiohttp.ClientSession(trust_env=True) as session:
            video_name = title if title else None
            photos, videos, attachments = await self._upload_media(photos, videos, attachments, session, video_name)

            url = f'https://api.vk.ru/method/wall.post'
            params = {
                'owner_id': '-' + self.group_id,
                'from_group': 1,
                'message': article,
                'attachments': ','.join(attachments),
                'access_token': self.token,
                'v': '5.199'
            }

            if delayed_post_date:
                params['publish_date'] = int(delayed_post_date)

            await self._post_request(params, session, url)

            # If the number of media files is more than 10, send the remaining files
            if photos or videos:
                params['message'] = ' '
                while photos or videos:
                    attachments = []
                    photos, videos, attachments = await self._upload_media(photos, videos, attachments, session)
                    params['attachments'] = ','.join(attachments)
                    await self._post_request(params, session, url)
            return

    async def repost(self, link: str) -> None:
        """
        Reposts a post from a link like "https://vk.com/wall-123_456" to a specified group
        :param link: Link to post
        :return: None
        """
        if not link.startswith('https://vk.'):
            raise ValueError('Invalid vk link')

        self.result = ''
        obj =  link.split(sep='/')[-1]  # extract from link string like "wall-1337_228"

        async with aiohttp.ClientSession(trust_env=True) as session:
            url = f'https://api.vk.ru/method/wall.repost'
            params = {
                'object': obj,
                'group_id': self.group_id,
                'access_token': self.token,
                'v': '5.199'
            }

            await self._post_request(params, session, url)

    async def _post_request(self, params: dict, session: aiohttp.ClientSession, url: str) -> None:
        """
        Makes a request to VK based on the given parameters
        :param params: Request parameters
        :param session: aiohttp.ClientSession object
        :param url: URL of API method
        :return: None
        """
        data = None
        try:
            async with session.post(url, data=params, ssl=False) as response:
                data = await response.read()
                data = json.loads(data)

                if 'error' in data:
                    raise Exception(data["error"]["error_msg"])

                self.result += f'https://vk.ru/wall-{self.group_id}_{data["response"]["post_id"]}'

        except json.decoder.JSONDecodeError:
            if data:
                # Extracting title from error html page
                match = re.search('<title>(.*?)</title>', data.decode(encoding='utf-8'), re.DOTALL)
                error_text = match.group(1) if match else 'Неизвестная ошибка'
            else:
                error_text = 'Неизвестная ошибка'
            self.result += f'Проблема отправки статьи в VK: {error_text}\n'
        except Exception as e:
            self.result += f'Проблема отправки статьи в VK: {str(e)}\n'

    async def _upload_media(
            self, pics: list, vids: list, attachmnts: list,
            session: aiohttp.ClientSession, video_name:str = None
    ) -> tuple:
        """
        Determines the order in which photos and videos are loaded
        :param pics: List of photo paths
        :param vids: List of video paths
        :param attachmnts: List of previously uploaded media
        :param session: aiohttp.ClientSession object
        :param video_name: Custom name of uploaded video
        :return: List of not uploaded photos, videos and list of ID's uploaded media
        """
        if ceil((len(pics) + len(vids)) / 10) == 1:
            if vids:
                for vid in vids:
                    attachmnts += await self._upload_video(vid, session, video_name)
                vids = []
            if pics:
                attachmnts += await self._upload_photos(pics, session)
                pics = []
        else:
            # First 10 items are sent first, after sending all the others
            sizeof_media = 10
            if vids:
                if len(vids) <= 10:
                    for vid in vids:
                        attachmnts += await self._upload_video(vid, session)
                    sizeof_media -= len(vids)
                    vids = []
                else:
                    for vid in vids[:10]:
                        attachmnts += await self._upload_video(vid, session)
                    sizeof_media = 0
                    vids = vids[10:]

            if pics:
                if len(pics) <= sizeof_media:
                    attachmnts += await self._upload_photos(pics, session)
                    pics = []
                else:
                    attachmnts += await self._upload_photos(pics[:sizeof_media], session)
                    pics = pics[sizeof_media:]

        return pics, vids, attachmnts

    async def _upload_photos(self, photos: list[str], session: aiohttp.ClientSession) -> list[str]:
        """
        Main method for uploading photos to VK
        :param photos: List of photo paths
        :param session: aiohttp.ClientSession object
        :return: List of id's of successfully uploaded photos
        """
        attachments = []
        upload_url = f'https://api.vk.ru/method/photos.getWallUploadServer'
        params = {
            'group_id': self.group_id,
            'access_token': self.token,
            'v': '5.131'
        }

        try:
            async with session.get(upload_url, params=params, ssl=False) as response:
                data = await response.json()
                if 'error' in data:
                    raise Exception(f'Ошибка получения URL для загрузки фото {data["error"]["error_msg"]}')
                else:
                    upload_url = data['response']['upload_url']

            # Splitting all photos into batches for avoid "Too many requests" error
            batch_size = 5
            photo_batches = [photos[i:i + batch_size] for i in range(0, len(photos), batch_size)]
            for batch_index, batch in enumerate(photo_batches, 1):
                upload_tasks = [self._upload_photo_to_server(p, upload_url, session) for p in batch]
                upload_results = await asyncio.gather(*upload_tasks)

                for result in upload_results:
                    if not result:
                        continue
                    attach = await self._save_photo(result, session)
                    if attach:
                        attachments.append(attach)

                if batch_index < len(photo_batches):
                    await asyncio.sleep(1)

            return attachments

        except Exception as e:
            self.result += f'Проблема отправки фото в VK: {str(e)}\n'
            return []

    async def _upload_photo_to_server(self, photo: str, upload_url: str, session: aiohttp.ClientSession) -> dict:
        """
        Uploads a photo to upload_url and returns the data for later saving
        :param photo: Path to photo
        :param upload_url: URL obtained by the method photos.getWallUploadServer
        :param session: aiohttp.ClientSession object
        :return: Data for later saving by self._save_photo method
        """
        try:
            form = aiohttp.FormData()
            async with aiofiles.open(photo, 'rb') as f:
                mime_type, _ = mimetypes.guess_type(photo)
                if mime_type is None:
                    mime_type = 'application/octet-stream'

                form.add_field(
                    'photo',
                    await f.read(),
                    filename=photo,
                    content_type=mime_type
                )

            async with session.post(upload_url, data=form, ssl=False) as response:
                text = await response.text()

            data = json.loads(text)
            if 'photo' not in data:
                raise Exception(f"photo undefined (ответ: {data})")

            return data
        except Exception as e:
            self.result += f'Проблема загрузки фото в VK: "{photo}": {str(e)}\n'
            return {}

    async def _save_photo(self, upload_data: dict, session: aiohttp.ClientSession) -> str | None:
        """
        Save photo by photos.saveWallPhoto method
        :param upload_data: Data of uploaded photo
        :param session: aiohttp.ClientSession object
        :return: ID of saved photo
        """
        try:
            save_url = 'https://api.vk.ru/method/photos.saveWallPhoto'
            params = {
                'group_id': self.group_id,
                'photo': upload_data['photo'],
                'server': upload_data['server'],
                'hash': upload_data['hash'],
                'access_token': self.token,
                'v': '5.131'
            }

            async with session.get(save_url, params=params, ssl=False) as response:
                data = await response.json()

            if 'error' in data:
                raise Exception(data['error']['error_msg'])

            photo_info = data['response'][0]
            return f"photo{photo_info['owner_id']}_{photo_info['id']}"
        except Exception as e:
            self.result += f'Ошибка сохранения фото в VK: {str(e)}\n'
            return None

    async def _upload_video(self, video: str, session: aiohttp.ClientSession, name: str = None,) -> list:
        """
        Uploads and saves a video in VK
        :param video: Path to video
        :param session: aiohttp.ClientSession object
        :param name: Custom name of video
        :return: ID of uploaded video
        """
        url = 'https://api.vk.ru/method/video.save'
        params = {
            'access_token': self.token,
            'group_id': self.group_id,
            'v': '5.199'
        }
        if name:
            params['name'] = name

        attachments = []

        try:
            async with session.get(url, params=params, ssl=False) as response:
                data = await response.json()
                if 'error' in data:
                    raise Exception(f'Ошибка получения URL для загрузки видео: {data["error"]["error_msg"]}')
                else:
                    upload_url = data['response']['upload_url']

            mime_type, _ = mimetypes.guess_type(video)
            if mime_type is None:
                mime_type = 'video/mp4'

            form = aiohttp.FormData()
            async with aiofiles.open(video, 'rb') as f:
                form.add_field(
                    'video_file',
                    await f.read(),
                    filename=video,
                    content_type=mime_type
                )

            async with session.post(upload_url, data=form, ssl=False) as response:
                data = await response.json()
                if 'error' in data:
                    raise Exception(f'Проблема загрузки видео: {data["error"]["error_msg"]}')
                else:
                    video_id = data['video_id']
                    owner_id = data['owner_id']
                    attachments.append(f'video{owner_id}_{video_id}')

            return attachments

        except Exception as e:
            self.result += f'Проблема отправки видео в VK: {str(e)}\n'
            return []