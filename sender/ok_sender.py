import json
from typing import Optional, List
from pathlib import Path

import aiohttp

from sender.sender import Sender


class OkSender(Sender):
    def __init__(self, access_token=None, application_key=None, application_secret_key=None, group_id=None):
        self.access_token = access_token
        self.application_key = application_key
        self.application_secret_key = application_secret_key
        self.group_id = group_id
        self.result = ''
        self.api_url = 'https://api.ok.ru/fb.do'

    def _concat_result(self, text: str) -> None:
        """If result is not empty, appends new line symbol to the value, otherwise just appends the value to result"""
        if self.result:
            self.result += '\n'
        self.result += text

    async def _upload_photo(self, session: aiohttp.ClientSession, photo_paths: List[str]) -> Optional[List[str]]:
        """Async upload photos through API OK.ru"""
        if not photo_paths:
            return None

        opened_photos = []

        try:
            params = {
                'application_key': self.application_key,
                'access_token': self.access_token,
                'method': 'photosV2.getUploadUrl',
                'count': len(photo_paths),
                'gid': self.group_id
            }

            async with session.get(self.api_url, params=params) as resp:
                result = await resp.json()
                if 'error' in result:
                    raise Exception(f"GetUploadUrl error: {result['error_msg']}")

                upload_url = result['upload_url']
                photo_ids = result['photo_ids']

            data = aiohttp.FormData()
            for idx, path in enumerate(photo_paths, start=1):
                file = open(path, 'rb')
                data.add_field(f"pic{idx}", file)
                opened_photos.append(file)

            async with session.post(upload_url, data=data) as up:
                photo_res = await up.text('utf-8')
                photo_res = json.loads(photo_res)['photos']

            tokens = []
            for pid in photo_ids:
                tokens.append(photo_res[pid]['token'])

            return tokens

        except Exception as e:
            exception_text = f"Photo upload error: {str(e)}"
            print(exception_text)
            self._concat_result(exception_text)

            return None
        finally:
            for f in opened_photos:
                if hasattr(f, 'close'):
                    f.close()

    async def _upload_video(self, session: aiohttp.ClientSession, video_path: str) -> Optional[str]:
        """Upload 1 video to OK.ru and return video ID"""
        try:
            params = {
                'application_key': self.application_key,
                'access_token': self.access_token,
                'method': 'video.getUploadUrl',
                'gid': self.group_id,
                'file_name': Path(video_path).name,
                'file_size': 0,
                'post_form': 'True'
            }

            async with session.get(self.api_url, params=params) as response:
                upload_data = await response.json()
                if 'error' in upload_data:
                    raise Exception(f"Error getting video upload URL: {upload_data['error_msg']}")

                upload_url = upload_data['upload_url']
                video_id = upload_data['video_id']

            with open(video_path, 'rb') as file:
                files = {'video': file}
                async with session.post(upload_url, data=files) as upload_response:
                    await upload_response.text('utf-8')

            return video_id

        except Exception as e:
            exception_text = f"Error uploading video: {e}"
            print(exception_text)
            self._concat_result(exception_text)

            return None

    async def send_article(
            self,
            title: str = '',
            text: str = '',
            photos: Optional[List[str]] = None,
            videos: Optional[List[str]] = None,
            delayed_post_date: Optional[int] = None
    ) -> None:
        """
        Publishes article in OK.ru
        :param title: Article title
        :param text: Article text
        :param photos: List of paths to photos
        :param videos: List of video paths
        :param delayed_post_date: Unix timestamp for delayed publication
        :return: Publish result or error log
        """
        await super().send_article(title=title, text=text, photos=photos, videos=videos)

        if photos is None:
            photos = []
        if videos is None:
            videos = []

        article = f'{title}\n\n{text}' if title else text

        attachments = {
            'media': [
                {
                    'type': 'text',
                    'text': article
                }
            ]
        }

        if delayed_post_date:
            attachments['publishAtMs'] = delayed_post_date * 1000

        async with aiohttp.ClientSession() as session:
            video_ids = []
            for video_path in videos:
                video_id = await self._upload_video(session, video_path)
                if video_id:
                    video_ids.append(video_id)
            if video_ids:
                attachments['media'].append({'type': 'movie', 'list': [{'id': i} for i in video_ids]})

            photo_tokens = await self._upload_photo(session, photos) if photos else []
            if photo_tokens:
                attachments['media'].append({'type': 'photo', 'list': [{'id': i} for i in photo_tokens]})

            params = {
                'application_key': self.application_key,
                'access_token': self.access_token,
                'method': 'mediatopic.post',
                'gid': self.group_id,
                'type': 'GROUP_THEME',
                'attachment': json.dumps(attachments) if attachments else None,
                'format': 'json'
            }

            params = {k: v for k, v in params.items() if v is not None}

            try:
                async with session.get(self.api_url, params=params) as response:
                    result = await response.text('utf-8')
                    if 'error' in result:
                        error_msg = json.loads(result)['error_msg']
                        raise Exception(error_msg)

                    result = result.replace('"', '')
                    self._concat_result(f'https://ok.ru/group/{self.group_id}/topic/{result}')
                    print(self.result)

            except Exception as e:
                exception_text = f"Error posting article: {e}"
                print(exception_text)
                self._concat_result(exception_text)
