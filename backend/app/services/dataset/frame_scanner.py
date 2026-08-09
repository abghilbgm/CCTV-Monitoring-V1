from pathlib import Path
from app.services.dataset.models import (
   DatasetSummary,
   CameraStatistics,
   VideoStatistics,
)

class FrameScanner:
   def __init__(self, raw_frames_root):
       self.raw_frames_root = Path(raw_frames_root)
   def scan(self):
       dataset = DatasetSummary()
       for camera_folder in sorted(self.raw_frames_root.iterdir()):
           if not camera_folder.is_dir():
               continue
           camera = CameraStatistics(
               camera_name=camera_folder.name
           )
           for video_folder in sorted(camera_folder.iterdir()):
               if not video_folder.is_dir():
                   continue
               images = sorted(video_folder.glob("*.jpg"))
               video = VideoStatistics(
                   camera_name=camera_folder.name,
                   video_name=video_folder.name,
                   video_path=Path(),
                   frame_directory=video_folder,
                   extracted_frames=len(images)
               )
               camera.videos.append(video)
           camera.total_videos = len(camera.videos)
           camera.extracted_frames = sum(
               video.extracted_frames
               for video in camera.videos
           )
           dataset.total_videos += camera.total_videos
           dataset.extracted_frames += camera.extracted_frames
           dataset.cameras.append(camera)
       dataset.total_cameras = len(dataset.cameras)
       return dataset
