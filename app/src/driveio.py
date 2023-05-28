import io
from dataclasses import dataclass

import pandas as pd
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from config.variables import Columns
from drive import service
from util import trim_date_and_remove_tz


def _load_folder(folder: str, drive=service) -> list:
    """
    Args:
        folder: name of the folder in google.drive
        drive: connector to google.drive API
    Returns: list of items in folder
    """
    results = drive.files().list(q=f"'{folder}' in parents",
                                   # pageSize=10,
                                   fields="nextPageToken, "
                                          "files(id, name, modifiedTime)"
                                 ).execute()
    items = results.get('files', [])
    return items


def get_folder_table(folder: str) -> pd.DataFrame:

    files_table = pd.DataFrame(_load_folder(folder=folder))

    if 'modifiedTime' in files_table.columns:
        files_table['modifiedTime'] = trim_date_and_remove_tz(files_table['modifiedTime'])
        files_table.sort_values(by='modifiedTime', ascending=False, inplace=True)

    return files_table


def get_files_dict(folder) -> dict:

    results = service.files().list(q=f"'{folder}' in parents",
                                   # pageSize=10,
                                   fields="nextPageToken, "
                                          "files(id, name, modifiedTime)"
                                   ).execute()
    items = results.get('files', [])

    files_table = pd.DataFrame(items)

    if 'modifiedTime' in files_table.columns:
        files_table['modifiedTime'] = pd.to_datetime(files_table['modifiedTime'])

    return files_table.to_dict()


def _download_file(file_id: str, drive=service) -> io.BytesIO:
    """
    Args:
        file_id: id of the file in google.drive
        drive: connector to google.drive API
    Returns: byte-stream of the file contents
    """
    try:
        request = drive.files().get_media(fileId=file_id)
        file_iostream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_iostream, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file_iostream = None

    return file_iostream


@dataclass
class File:

    id: str
    name: str
    modified: pd.Timestamp

    def _format_dataframe(self):
        self.data[Columns.DATE] = trim_date_and_remove_tz(self.data[Columns.DATE])
        self.data[Columns.AMOUNT].replace(to_replace='-', value='0', inplace=True)
        self.data[Columns.AMOUNT] = self.data[Columns.AMOUNT].astype('float')

    def __post_init__(self):
        iostream = _download_file(file_id=self.id)
        iostream.seek(0)
        self.data = pd.read_csv(iostream)
        self._format_dataframe()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'File ({self.name}, {self.id}, r/c: {self.data.shape})'


def get_file(folder: pd.DataFrame, name: str) -> File:

    filtered = folder[folder['name'].str.contains(name)]
    if filtered.shape[0] == 0:
        raise FileNotFoundError('File not found in Google Drive')
    file_metadata = filtered.sort_values(by='modifiedTime', ascending=False).iloc[0]
    file = File(id=file_metadata['id'], name=file_metadata['name'], modified=file_metadata['modifiedTime'])

    return file
