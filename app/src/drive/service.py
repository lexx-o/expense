from googleapiclient.discovery import build

from .credentials import credentials


service = build('drive', 'v3', credentials=credentials)
