from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

VIDEO_ROOT = Path(os.getenv("VIDEO_ROOT"))
FRAME_OUTPUT = Path(os.getenv("FRAME_OUTPUT"))
METADATA_OUTPUT = Path(os.getenv("METADATA_OUTPUT"))
FRAME_INTERVAL = int(os.getenv("FRAME_INTERVAL"))
IMAGE_FORMAT = os.getenv("IMAGE_FORMAT")
