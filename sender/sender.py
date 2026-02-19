from abc import ABC, abstractmethod
import re


class Sender(ABC):
    @abstractmethod
    async def send_article(self, title='', text='', photos=None, videos=None):
        pass

    def _split_into_chunks(self, text: str, chunk_size: int = 4096) -> list:
        """
        Splits input text into semantically meaningful chunks of specified maximum size.
        :param text: Input string to be split into chunks.
        :param chunk_size: Maximum character length of each chunk (default: 4096).
        :return: List of text chunks
        """
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