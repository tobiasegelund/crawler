import os
import logging
import datetime
from pathlib import Path

from dotenv import load_dotenv

# Load .env variables
try:
    load_dotenv()
except IOError:
    pass

logging.basicConfig(format="%(asctime)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today()
TODAY_STR = TODAY.strftime("%Y%m%d")

IMAGE_TAGS = ("img", "source", "picture")
VIDEO_TAGS = (
    "video",
    "source",
    'source[type="application/x-mpegURL"]',
    'source[type="video/mp4"]',
    "href",
)
AUDIO_TAGS = ("audio", "source", "a")

IMAGE_EXTENSIONS = (
    ".jpg",
    ".gif",
    ".png",
    ".bmp",
    ".svg",
    ".webp",
    ".ico",
    ".jpeg",
    ".bat",
    ".heif",
    ".jfif",
    ".pjpeg",
    ".pjp",
    ".svg",
    ".webp",
)
VIDEO_EXTENSION = (
    ".mp4",
    ".webm",
    ".mkv",
    ".flv",
    ".vob",
    ".ogg",
    ".ogv",
    ".gif",
    ".gifv",
    ".drc",
    ".flv",
    ".f4v",
    ".f4p",
    ".f4a",
    ".f4b",
    ".m4v",
    ".mpg",
    ".mpeg",
    ".m2v",
    ".svi",
    ".3gp",
    ".mxf",
    ".roq",
    ".amv",
    ".asf",
    ".avi",
    ".mng",
    ".viv",
    ".rmvb",
    ".wmv",
    ".mov",
    ".qt",
)
AUDIO_EXTENTIONS = (
    ".3gp",
    ".aa",
    ".aac",
    ".aax",
    ".act",
    ".aiff",
    ".alac",
    ".amr",
    ".ape",
    ".au",
    ".awb",
    ".dss",
    ".dvf",
    ".flac",
    ".gsm",
    ".iklax",
    ".ivs",
    ".m4a",
    ".m4b",
    ".m4p",
    ".mmf",
    ".mp3",
    ".mpc",
    ".msv",
    ".nmf",
    ".ogg",
    ".oga",
    ".mogg",
    ".opus",
    ".ra",
    ".rm",
    ".raw",
    ".rf64",
    ".sln",
    ".tta",
    ".voc",
    ".vox",
    ".wav",
    ".wma",
    ".wv",
    ".webm",
    ".8svx",
    ".cda",
)

# DEBUG_MODE = True if bool(os.environ.get("DEBUG_MODE")) is True else False
