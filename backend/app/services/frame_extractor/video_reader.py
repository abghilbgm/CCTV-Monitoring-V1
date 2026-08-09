import cv2
from pathlib import Path

class VideoReader:
   def __init__(self, video_path):
       self.video_path = Path(video_path)
       self.capture = None

   def open(self):
       self.capture = cv2.VideoCapture(str(self.video_path))
       if not self.capture.isOpened():
           raise Exception(f"Unable to open video: {self.video_path}")
       return self.capture

   def get_fps(self):
       return self.capture.get(cv2.CAP_PROP_FPS)

   def get_total_frames(self):
       return int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))

   def get_duration(self):
       fps = self.get_fps()
       if fps == 0:
           return 0
       return self.get_total_frames() / fps
       
   def release(self):
       if self.capture:
           self.capture.release()
