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
VIDEO_TAGS = ("video", "source")
AUDIO_TAGS = ()

IMAGE_EXTENSIONS = (".jpg", ".gif", ".png", ".bmp", ".svg", ".webp", ".ico")
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
    ".MTS",
    ".M2TS",
    ".TS",
)
AUDIO_EXTENTIONS = ()

# DEBUG_MODE = True if bool(os.environ.get("DEBUG_MODE")) is True else False
