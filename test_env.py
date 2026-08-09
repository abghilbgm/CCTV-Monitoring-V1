from dotenv import load_dotenv
import os

load_dotenv()

print("VIDEO_ROOT =", os.getenv("VIDEO_ROOT"))
print("FRAME_OUTPUT =", os.getenv("FRAME_OUTPUT"))
print("METADATA_OUTPUT =", os.getenv("METADATA_OUTPUT"))
print("IMAGE_FORMAT =", os.getenv("IMAGE_FORMAT"))
