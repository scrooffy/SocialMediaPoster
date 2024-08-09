import re
import json
from math import ceil
import aiohttp
from sender.sender import Sender


class VkSender(Sender):
    # Generate token link:
    # https://oauth.vk.com/authorize?client_id=<app_id>&redirect_uri=https://api.vk.com/blank.html
    # &scope=offline,wall,photos,video&response_type=token
    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.result = ''

    async def send_article(self, title='', text='', photos=None, videos=None, delayed_post_date=None):
        await super().send_article(title=title, text=text, photos=photos, videos=videos)
        if videos is None:
            videos = []
        if photos is None:
            photos = []
        self.result = ''
        article = f'{title}\n\n{text}' if title else text
        attachments = []

        async with aiohttp.ClientSession(trust_env=True) as session:
            photos, videos, attachments = await self.upload_media(photos, videos, attachments, session)

            url = f'https://api.vk.com/method/wall.post'
            params = {
                'owner_id': '-' + self.group_id,
                'from_group': 1,
                'message': article,
                'attachments': ','.join(attachments),
                'access_token': self.token,
                'v': '5.199'
            }

            if delayed_post_date:
                params['publish_date'] = delayed_post_date

            await self.post_request(params, session, url, return_link=True)

            if photos or videos:
                params['message'] = ' '
                while photos or videos:
                    attachments = []
                    photos, videos, attachments = await self.upload_media(photos, videos, attachments, session)
                    params['attachments'] = ','.join(attachments)
                    await self.post_request(params, session, url)
            return self.result

    async def post_request(self, params, session, url, return_link=False):
        async with session.post(url, data=params, ssl=False) as response:
            data = await response.read()
            post_id = None
            error_text = None

            try:
                data = json.loads(data)
                if 'error' in data:
                    error_text = data["error"]["error_msg"]
                else:
                    post_id = data["response"]["post_id"]
            except json.decoder.JSONDecodeError:
                # Extracting title from error html page
                match = re.search('<title>(.*?)</title>', data.decode(encoding='utf-8'), re.DOTALL)
                error_text = match.group(1) if match else 'Неизвестная ошибка'
            except Exception as e:
                error_text = str(e)

            if post_id:
                if return_link:
                    self.result += f'https://vk.com/wall-{self.group_id}_{post_id}'
            elif error_text:
                self.result += f'Проблема отправки статьи в VK: {error_text}'
            else:
                self.result += 'Что то определенно не так c VK ☉ ‿ ⚆'

    async def upload_media(self, pics, vids, attachmnts, session):
        if ceil((len(pics) + len(vids)) / 10) == 1:
            if vids:
                for vid in vids:
                    attachmnts += await self.upload_video(vid, session)
                vids = []
            if pics:
                attachmnts += await self.upload_photos(pics, session)
                pics = []
        else:
            # First 10 items are sent first, after sending all the others
            sizeof_media = 10
            if vids:
                if len(vids) <= 10:
                    for vid in vids:
                        attachmnts += await self.upload_video(vid, session)
                    sizeof_media -= len(vids)
                    vids = []
                else:
                    for vid in vids[:10]:
                        attachmnts += await self.upload_video(vid, session)
                    sizeof_media = 0
                    vids = vids[10:]

            if pics:
                if len(pics) <= sizeof_media:
                    attachmnts += await self.upload_photos(pics, session)
                    pics = []
                else:
                    attachmnts += await self.upload_photos(pics[:sizeof_media], session)
                    pics = pics[sizeof_media:]

        return [pics, vids, attachmnts]

    async def upload_photos(self, photos, session):
        attachments = []
        upload_url = f'https://api.vk.com/method/photos.getWallUploadServer'
        params = {
            'group_id': self.group_id,
            'access_token': self.token,
            'v': '5.131'
        }

        async with session.get(upload_url, params=params, ssl=False) as response:
            data = await response.json()
            if 'error' in data:
                self.result += f'Проблема отправки фото в VK: {data["error"]["error_msg"]}\n'
                return []
            else:
                upload_url = data['response']['upload_url']

        for photo in photos:
            async with session.post(upload_url, data={'photo': open(photo, 'rb')}, ssl=False) as response:
                data = await response.text()
                data = json.loads(data)

            if 'error' in data:
                self.result += f'Проблема отправки фото в VK: {data["error"]["error_msg"]}\n'
                continue

            save_url = f'https://api.vk.com/method/photos.saveWallPhoto'
            params = {
                'group_id': self.group_id,
                'photo': data['photo'],
                'server': data['server'],
                'hash': data['hash'],
                'access_token': self.token,
                'v': '5.131'
            }

            async with session.get(save_url, params=params, ssl=False) as response:
                data = await response.text()
                data = json.loads(data)

            if 'error' in data:
                self.result += f'Проблема отправки фото в VK: {data["error"]["error_msg"]}\n'
                continue

            photo_id = data['response'][0]['id']
            owner_id = data['response'][0]['owner_id']
            attachments.append(f'photo{owner_id}_{photo_id}')

        return attachments

    async def upload_video(self, video, session):
        url = 'https://api.vk.com/method/video.save'
        params = {
            'access_token': self.token,
            'group_id': self.group_id,
            'v': '5.199'
        }
        attachments = []

        async with session.get(url, params=params, ssl=False) as response:
            data = await response.json()
            if 'error' in data:
                self.result += f'Проблема отправки видео в VK: {data["error"]["error_msg"]}\n'
                return []
            else:
                upload_url = data['response']['upload_url']

        async with session.post(upload_url, data={'video_file': open(video, 'rb')}, ssl=False) as response:
            data = await response.json()
            if 'error' in data:
                self.result += f'Проблема отправки видео в VK: {data["error"]["error_msg"]}\n'
            else:
                video_id = data['video_id']
                owner_id = data['owner_id']
                attachments.append(f'video{owner_id}_{video_id}')

        return attachments
