from abc import ABC, abstractmethod


class Sender(ABC):
    @abstractmethod
    async def send_article(self, title='', text='', photos=None, videos=None):
        pass
