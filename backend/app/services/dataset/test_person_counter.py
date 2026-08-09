from pathlib import Path
from app.services.dataset.person_counter import PersonCounter

MODEL_PATH = "backend/app/models/yolov8n.pt"
IMAGE_PATH = Path(
   "dataset/raw_frames"
)
counter = PersonCounter(MODEL_PATH)
found = False
for camera in IMAGE_PATH.iterdir():
   if not camera.is_dir():
       continue
   for video in camera.iterdir():
       if not video.is_dir():
           continue
       images = sorted(video.glob("*.jpg"))
       if len(images) == 0:
           continue
       image = images[0]
       count = counter.count_people(image)
       print(f"{image.name} -> {count} persons")
       found = True
       break
   if found:
       break

