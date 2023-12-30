import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        """Инициализация Video"""
        api_key = os.getenv('API_key')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_info = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()
        video_data = video_info['items'][0]
        self.id = video_id
        self.title = video_data['snippet']['title']
        self.video_url = f"https://www.youtube.com/watch?v={video_id}"
        self.view_count = int(video_data['statistics']['viewCount'])
        self.like_count = int(video_data['statistics']['likeCount'])

    def __str__(self):
        """Информация для пользователя"""
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """Инициализация PLVideo"""
        super().__init__(video_id)
        self.playlist_id = playlist_id
