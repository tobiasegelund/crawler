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

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today()
TODAY_STR = TODAY.strftime("%Y%m%d")


IMAGE_TYPES = [".jpg", ".png"]
VIDEO_TYPES = []
ADUIO_TYPES = []

DEBUG_MODE = True if bool(os.environ.get("DEBUG_MODE")) is True else False
