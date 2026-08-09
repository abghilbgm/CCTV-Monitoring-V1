from app.services.dataset.person_counter import PersonCounter
from app.services.dataset.models import DatasetSummary

class DatasetAnalyzer:
   def __init__(self, model_path: str):
       self.counter = PersonCounter(model_path)
   def analyze(self, dataset: DatasetSummary):
       print("\n========== ANALYZING DATASET ==========\n")
       for camera in dataset.cameras:
           print(f"Camera : {camera.camera_name}")
           for video in camera.videos:
               person_frames = 0
               total_persons = 0
               max_persons = 0
               image_paths = sorted(
                   video.frame_directory.glob("*.jpg")
               )
               for image in image_paths[:200]:
                   count = self.counter.count_people(image)
                   if count > 0:
                       person_frames += 1
                   total_persons += count
                   max_persons = max(max_persons, count)
               video.person_frames = person_frames
               video.total_persons = total_persons
               video.max_persons_in_frame = max_persons
               if video.extracted_frames > 0:
                   video.activity_score = (
                       total_persons /
                       video.extracted_frames
                   )
               print(
                   f"Analyzing {camera.camera_name} -> "
                   f"{video.video_name} "
                   f"({video.extracted_frames} frames)"
               )
               camera.person_frames += person_frames
               camera.total_persons += total_persons
               camera.max_persons = max(
                   camera.max_persons,
                   max_persons
               )
           if camera.extracted_frames > 0:
               camera.activity_score = (
                   camera.total_persons /
                   camera.extracted_frames
               )
       return dataset

