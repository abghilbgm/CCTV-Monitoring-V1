from pathlib import Path
import shutil
from app.services.dataset.models import DatasetSummary

class DatasetSelector:
   def __init__(self, output_directory):
       self.output_directory = Path(output_directory)
   def select(self, dataset: DatasetSummary):
       print("\n========== SELECTING FRAMES ==========\n")
       for camera in dataset.cameras:
           for video in camera.videos:
               if video.recommended_frames <= 0:
                   continue
               images = sorted(
                   video.frame_directory.glob("*.jpg")
               )
               if not images:
                   continue
               step = max(
                   1,
                   len(images) // video.recommended_frames
               )
               destination = (
                   self.output_directory /
                   camera.camera_name /
                   video.video_name
               )
               destination.mkdir(
                   parents=True,
                   exist_ok=True
               )
               copied = 0
               for image in images[::step]:
                   shutil.copy2(
                       image,
                       destination / image.name
                   )
                   copied += 1
                   if copied >= video.recommended_frames:
                       break
               print(
                   f"{camera.camera_name} | "
                   f"{video.video_name} -> "
                   f"{copied} frames selected"
               )
