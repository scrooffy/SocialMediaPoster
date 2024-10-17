import json
from typing import Any
# from pathlib import Path

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
            application_secret_key=application_secret_key,
        )

        self.result = ''
        self.links = None

    async def send_article(self, title='', text='', photos=None, videos=None, delayed_post_date=None, get_links=False,
                           return_links=False) -> dict | None:
        await super().send_article(title=title, text=text, photos=photos, videos=videos)
        self.result = ''
        self.links = {
            'photos': [],
            'videos': []
        }

        upload = Upload(self.ok_api)

        article = f'{title}\n\n{text}' if title else text

        attachments = {
            'media': [
                {
                    'type': 'text',
                    'text': article
                }
            ]
        }

        # if videos:
        #     videos_media_attachments: dict[str, str | list[Any]] = {
        #             'type': 'movie',
        #             'list': []
        #         }
        #
        #     for video in videos:
        #         title = Path(video).stem
        #         ext = title = Path(video).name
        #         file_size = Path(video).stat().st_size
        #         upload_response = upload.video(video=video, file_name=title, file_size=file_size, gid=self.group_id, post_form=True, attachment_type= 'MOVIE')
        #         response = self.ok_api.video.update(vid=upload_response['video_id'], title=title, best_thumbnail_index=1, privacy='PUBLIC')
        #         videos_media_attachments['list'].append({'id': upload_response['video_id']})
        #
        #     attachments['media'].append(videos_media_attachments)

        if photos:
            photos_media_attachments: dict[str, str | list[Any]] = {
                    'type': 'photo',
                    'list': []
                }
            upload_response = upload.photo(photos=photos, group_id=self.group_id)
            photo_tokens = [upload_response['photos'][i]['token'] for i in upload_response['photos']]

            [photos_media_attachments['list'].append({'id': i}) for i in photo_tokens]

            attachments['media'].append(photos_media_attachments)

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

        return self.links if return_links else None
