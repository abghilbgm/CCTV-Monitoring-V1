import cv2
from pathlib import Path
from app.core.settings import FRAME_INTERVAL
from app.services.dataset.models import VideoStatistics

class VideoStatisticsAnalyzer:
   def analyze(self, video: VideoStatistics):
       capture = cv2.VideoCapture(str(video.video_path))
       if not capture.isOpened():
           print(f"Cannot open {video.video_name}")
           return video
       video.total_frames = int(
           capture.get(cv2.CAP_PROP_FRAME_COUNT)
       )
       video.fps = capture.get(
           cv2.CAP_PROP_FPS
       )
       video.resolution_width = int(
           capture.get(cv2.CAP_PROP_FRAME_WIDTH)
       )
       video.resolution_height = int(
           capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
       )
       if video.fps > 0:
           video.duration_seconds = (
               video.total_frames /
               video.fps
           )
       video.extracted_frames = (
           video.total_frames //
           FRAME_INTERVAL
       )
       capture.release()
       return video
