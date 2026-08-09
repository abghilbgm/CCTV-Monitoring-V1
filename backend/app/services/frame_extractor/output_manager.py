from pathlib import Path

class OutputManager:
   def __init__(self, output_root):
       self.output_root = Path(output_root)

   def create_video_output_folder(self, camera_name, video_name):
       folder = (
           self.output_root
           / camera_name
           / video_name
       )
       folder.mkdir(parents=True, exist_ok=True)
       return folder
