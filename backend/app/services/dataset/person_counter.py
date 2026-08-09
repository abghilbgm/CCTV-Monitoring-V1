from ultralytics import YOLO
from app.services.dataset.config import (
   PERSON_CONFIDENCE,
   IMAGE_SIZE,
)

class PersonCounter:
   PERSON_CLASS = 0
   def __init__(self, model_path):
       self.model = YOLO(str(model_path))
       print("✓ Person Detection Model Loaded")
   def count_people(self, image_path):
       results = self.model.predict(
           source=str(image_path),
           conf=PERSON_CONFIDENCE,
           imgsz=IMAGE_SIZE,
           verbose=False,
       )
       result = results[0]
       person_count = 0
       for box in result.boxes:
           cls = int(box.cls.item())
           if cls == self.PERSON_CLASS:
               person_count += 1
       return person_count

