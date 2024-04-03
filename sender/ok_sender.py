import json
from typing import Any

from ok_api import OkApi, Upload
from sender.sender import Sender


class OkSender(Sender):
    def __init__(self, access_token=None, application_key=None, application_secret_key=None, group_id=None):
        self.access_token = access_token
        self.application_key = application_key
        self.application_secret_key = application_secret_key
        self.group_id = group_id

        self.ok_api = OkApi(
            access_token=access_token,
            application_key=application_key,
            application_secret_key=application_secret_key
        )

        self.result = ''

    async def send_article(self, title='', text='', photos=None, videos=None, delayed_post_date=None):
        await super().send_article(title=title, text=text, photos=photos, videos=videos)
        self.result = ''

        upload = Upload(self.ok_api)

        article = f'{title}\n\n{text}' if title else text
        # I don't have token access to VIDEO_CONTENT, that's why no uploading video here
        attachments = {
            'media': [
                {
                    'type': 'text',
                    'text': article
                }
            ]
        }

        if photos:
            photos_media_attachments: dict[str, str | list[Any]] = {
                    'type': 'photo',
                    'list': []
                }
            attachments['media'].append(photos_media_attachments)
            upload_response = upload.photo(photos=photos, group_id=self.group_id)
            photo_tokens = [upload_response['photos'][i]['token'] for i in upload_response['photos']]

            for photo_id in photo_tokens:
                attachments['media'][1]['list'].append({'id': photo_id})

        if delayed_post_date:
            attachments['publishAtMs'] = delayed_post_date * 1000

        post = self.ok_api.mediatopic.post(
            attachment=json.dumps(attachments),
            format='json',
            gid=self.group_id,
            type='GROUP_THEME'
        )
        response = post.content.decode("utf-8")
        if 'error' in response:
            response = json.loads(response)
            self.result = f'Проблема отправки статьи в Ok: {response["error_msg"]}'
        else:
            post_id = post.content.decode("utf-8").replace("\"", "")
            self.result = f'https://ok.ru/group/{self.group_id}/topic/{post_id}'

        return self.result
