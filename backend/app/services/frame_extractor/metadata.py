import csv
from pathlib import Path

class MetadataManager:
   def __init__(self, metadata_folder):
       self.metadata_folder = Path(metadata_folder)
       self.metadata_folder.mkdir(
           parents=True,
           exist_ok=True
       )
       self.csv_file = self.metadata_folder / "frame_metadata.csv"
       if not self.csv_file.exists():
           with open(
               self.csv_file,
               "w",
               newline=""
           ) as file:
               writer = csv.writer(file)
               writer.writerow([
                   "camera",
                   "video",
                   "frame_number",
                   "timestamp_seconds",
                   "image_path"
               ])
   def save(
           self,
           camera,
           video,
           frame,
           timestamp,
           image_path):
       with open(
               self.csv_file,
               "a",
               newline=""
       ) as file:
           writer = csv.writer(file)
           writer.writerow([
               camera,
               video,
               frame,
               timestamp,
               image_path
           ])
