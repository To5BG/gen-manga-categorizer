import os
from mangadex_downloader import MangaDexDownloader

manga_id = "efb4278c-a761-406b-9d69-19603c5e4c8b"
downloader = MangaDexDownloader(manga_id)

downloader.download_manga(start=210)
