import datetime
import os

DIR = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today()
TODAY_STR = TODAY.strftime("%Y%m%d")

IMAGE_TYPES = [".jpg", ".png"]
VIDEO_TYPES = []
