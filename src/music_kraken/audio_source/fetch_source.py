from ..utils.shared import *

from .sources import (
    youtube,
    musify,
    local_files
)

logger = URL_DOWNLOAD_LOGGER

# maps the classes to get data from to the source name
sources = {
    'Youtube': youtube.Youtube,
    'Musify': musify.Musify
}


class Download:
    def __init__(self) -> None:
        self.urls = []

        for row in database.get_tracks_without_src():
            row['artists'] = [artist['name'] for artist in row['artists']]

            id_ = row['id']
            if os.path.exists(os.path.join(MUSIC_DIR, row['file'])):
                logger.info(f"skipping the fetching of the download links, cuz {row['file']} already exists.")
                continue

            """
            not implemented yet, will in one point crashe everything
            # check File System
            file_path = file_system.get_path(row)
            if file_path is not None:
                self.add_url(file_path, 'file', id_)
                continue
            """
            """
            # check YouTube
            youtube_url = youtube.Youtube.fetch_source(row)
            if youtube_url is not None:
                self.add_url(youtube_url, 'youtube', id_)
                continue

            # check musify
            musify_url = musify.Musify.fetch_source(row)
            if musify_url is not None:
                self.add_url(musify_url, 'musify', id_)
                continue

            # check musify again, but with a different methode that takes longer
            musify_url = musify.get_musify_url_slow(row)
            if musify_url is not None:
                self.add_url(musify_url, 'musify', id_)
                continue
            """
            for src in AUDIO_SOURCES:
                res = Download.fetch_from_src(row, src)
                if res is not None:
                    Download.add_url(res, src, id_)

            logger.warning(f"Didn't find any sources for {row['title']}")

    @staticmethod
    def fetch_from_src(row: dict, src: str):
        if src not in sources:
            raise ValueError(f"source {src} seems to not exist")

        source_subclass = sources[src]
        return source_subclass.fetch_source(row)

    @staticmethod
    def add_url(url: str, src: str, id_: str):
        database.set_download_data(id_, url, src)


if __name__ == "__main__":
    download = Download()
