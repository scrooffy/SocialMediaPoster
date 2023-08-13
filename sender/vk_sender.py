import json
import aiohttp
from sender.sender_abs import Sender


class VkSender(Sender):
    # https://oauth.vk.com/authorize?client_id=51692513&redirect_uri=https://api.vk.com/blank.html&scope=offline,wall,photos,video&response_type=token
    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.result = ''

    async def send_article(self, title='', text='', photos=None, videos=None):
        await super().send_article(title=title, text=text, photos=photos, videos=videos)

        article = f'{title}\n\n{text}' if title else text
        attachments = []

        async with aiohttp.ClientSession() as session:
            if photos:
                attachments += await self.upload_photos(photos, session)
            if videos:
                attachments += await self.upload_video(videos, session)

            url = f'https://api.vk.com/method/wall.post'
            params = {
                'owner_id': '-' + self.group_id,
                'from_group': 1,
                'message': article,
                'attachments': ','.join(attachments),
                'access_token': self.token,
                'v': '5.131'
            }

            async with session.post(url, params=params) as response:
                response_result = await response.json()
                if 'error' in response_result:
                    self.result += f'Проблема отправки статьи в VK: {response_result["error"]["error_msg"]}'
                else:
                    self.result += f'https://vk.com/wall-{self.group_id}_{response_result["response"]["post_id"]}'

    async def upload_photos(self, photos, session):
        attachments = []
        upload_url = f'https://api.vk.com/method/photos.getWallUploadServer'
        params = {
            'group_id': self.group_id,
            'access_token': self.token,
            'v': '5.131'
        }

        async with session.get(upload_url, params=params) as response:
            data = await response.json()
            if 'error' in data:
                self.result += f'Проблема отправки фото в VK: {data["error"]["error_msg"]}\n'
                return []   # return None throw an error 'None type is not iterable'
            else:
                upload_url = data['response']['upload_url']

        for photo in photos:
            async with session.post(upload_url, data={'photo': open(photo, 'rb')}) as response:
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

            async with session.get(save_url, params=params) as response:
                data = await response.text()
                data = json.loads(data)

            if 'error' in data:
                self.result += f'Проблема отправки фото в VK: {data["error"]["error_msg"]}\n'
                continue

            photo_id = data['response'][0]['id']
            owner_id = data['response'][0]['owner_id']
            attachments.append(f'photo{owner_id}_{photo_id}')

        return attachments

    async def upload_video(self, videos, session):
        url = 'https://api.vk.com/method/video.save'
        params = {
            'access_token': self.token,
            'group_id': self.group_id,
            'v': '5.131'
        }
        attachments = []

        async with session.get(url, params=params) as response:
            data = await response.json()
            if 'error' in data:
                self.result += f'Проблема отправки видео в VK: {data["error"]["error_msg"]}\n'
                return []  # return None throws an error 'None type is not iterable'
            else:
                upload_url = data['response']['upload_url']

        for video in videos:
            async with session.post(upload_url, data={'video_file': open(video, 'rb')}) as response:
                data = await response.json()
                if 'error' in data:
                    self.result += f'Проблема отправки видео в VK: {data["error"]["error_msg"]}\n'
                    continue
                else:
                    video_id = data['video_id']
                    owner_id = data['owner_id']
                    attachments.append(f'video{owner_id}_{video_id}')

        return attachments
