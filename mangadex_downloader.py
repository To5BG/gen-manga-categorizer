import os
import requests

MANGADEX_API = "https://api.mangadex.org"


class MangaDexDownloader:
    def __init__(self, manga_id: str, save_path: str = "panels"):
        self.manga_id = manga_id
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    def get_chapters(self):
        url = f"{MANGADEX_API}/manga/{self.manga_id}/feed"
        response = requests.get(
            url,
            params={
                "translatedLanguage[]": "en",
                "order[chapter]": "asc",
                "limit": 500,
            },
        )
        return response.json().get("data") if response.status_code == 200 else []

    def get_pages(self, chapter_id: str):
        url = f"{MANGADEX_API}/at-home/server/{chapter_id}"
        response = requests.get(url)
        if response.status_code == 200:
            json = response.json()
            base = json.get("baseUrl") + "/data/" + json.get("chapter").get("hash")
            return base, json.get("chapter").get("data")
        return "", []

    def download_chapter(self, chapter):
        # Init
        chapter_number = chapter["attributes"].get("chapter", "unknown")
        base, pages = self.get_pages(chapter["id"])
        if not pages:
            print(f"No pages found for chapter {chapter_number}")
            return
        # Check if chapter is already downloaded
        chapter_path = os.path.join(self.save_path, f"chapter_{chapter_number}")
        if os.path.exists(chapter_path) and len(pages) == len(os.listdir(chapter_path)):
            print(f"Chapter {chapter_number} already downloaded")
            return
        # Download chapter
        os.makedirs(chapter_path, exist_ok=True)
        print(f"Downloading chapter {chapter_number}...")
        for page in pages:
            page_url = f"{base}/{page}"
            self.download_image(page_url, os.path.join(chapter_path, page))

    def download_image(self, url, save_path):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded {save_path}")
        else:
            print(f"Failed to download {url}")

    def download_manga(self):
        [self.download_chapter(chapter) for chapter in self.get_chapters()]
