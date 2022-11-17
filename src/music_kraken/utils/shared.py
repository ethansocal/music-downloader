import musicbrainzngs
import logging
import tempfile
import os

from .database import Database

TEMP_FOLDER = "music-downloader"
LOG_FILE = "download_logs.log"
DATABASE_FILE = "metadata.db"
DATABASE_STRUCTURE_FILE = "database_structure.sql"
DATABASE_STRUCTURE_FALLBACK = "https://raw.githubusercontent.com/HeIIow2/music-downloader/master/assets/database_structure.sql"
temp_dir = os.path.join(tempfile.gettempdir(), TEMP_FOLDER)
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)

# configure logger default
logging.basicConfig(
    level=logging.INFO,
    format=logging.BASIC_FORMAT,
    handlers=[
        logging.FileHandler(os.path.join(temp_dir, LOG_FILE)),
        logging.StreamHandler()
    ]
)

SEARCH_LOGGER = logging.getLogger("mb-cli")
DATABASE_LOGGER = logging.getLogger("database")
METADATA_DOWNLOAD_LOGGER = logging.getLogger("metadata")
URL_DOWNLOAD_LOGGER = logging.getLogger("AudioSource")
YOUTUBE_LOGGER = logging.getLogger("Youtube")
MUSIFY_LOGGER = logging.getLogger("Musify")
PATH_LOGGER = logging.getLogger("create-paths")
DOWNLOAD_LOGGER = logging.getLogger("download")
LYRICS_LOGGER = logging.getLogger("lyrics")
GENIUS_LOGGER = logging.getLogger("genius")

logging.getLogger("musicbrainzngs").setLevel(logging.WARNING)
musicbrainzngs.set_useragent("metadata receiver", "0.1", "https://github.com/HeIIow2/music-downloader")

NOT_A_GENRE = ".", "..", "misc_scripts", "Music", "script", ".git", ".idea"
MUSIC_DIR = os.path.expanduser('~/Music')


database = Database(os.path.join(temp_dir, DATABASE_FILE),
                    os.path.join(temp_dir, DATABASE_STRUCTURE_FILE),
                    DATABASE_STRUCTURE_FALLBACK,
                    DATABASE_LOGGER,
                    reset_anyways=False)


TOR = False
proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
} if TOR else {}

# only the sources here will get downloaded, in the order the list is ordered
AUDIO_SOURCES = ["Musify", "Youtube"]
