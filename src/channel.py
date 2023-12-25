import json
import os
import googleapiclient
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_key')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.info = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channel_id = channel_id
        self.get_channel_info()


    def __str__(self):
        "Информация о канале"
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        "Сложение"
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        "Вычитание"
        return self.subscribers - other.subscribers

    def __gt__(self, other):
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        return self.subscribers >= other.subscribers

    def __it__(self, other):
        return self.subscribers < other.subscribers


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.info, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    def get_channel_info(self):
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = self.api_key)
        request = youtube.channels().list(part="snippet, statistics", id = self.__channel_id)
        response = request.execute()
        if 'items' in response:
            channel_data = response['items'][0]
            self.id = self.__channel_id
            self.title = channel_data['snippet']['title']
            self.description = channel_data['snippet']['description']
            self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
            self.subscribers = int(channel_data['statistics']['subscriberCount'])
            self.video_count = int(channel_data['statistics']['videoCount'])
            self.view_count = int(channel_data['statistics']['viewCount'])
        else:
            print("Channel not found.")

    @classmethod
    def get_service(cls):
        api_key = os.getenv('API_key')
        return build("youtube", "v3", developerKey=api_key)

    def to_json(self, filename):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "link": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "view_count": self.view_count
     }

        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=2)
