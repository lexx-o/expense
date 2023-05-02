import io

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from drive import service


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


def _download_file(file_id: str, drive=service) -> io.BytesIO:
    """
    Args:
        file_id: id of the file in google.drive
        drive: connector to google.drive API
    Returns: byte-stream of the file contents
    """
    try:
        request = drive.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file
