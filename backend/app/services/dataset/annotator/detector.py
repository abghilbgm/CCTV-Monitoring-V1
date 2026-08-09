from pathlib import Path
from ultralytics import YOLO
from app.services.dataset.config import (
   PPE_MODEL,
   PPE_CONFIDENCE,
   IMAGE_SIZE,
)

class Detector:
   def __init__(self):
       self.model = YOLO(str(PPE_MODEL))
       print("✓ PPE Detection Model Loaded")
   def detect(self, image_path: Path):
       results = self.model.predict(
           source=str(image_path),
           conf=PPE_CONFIDENCE,
           imgsz=IMAGE_SIZE,
           verbose=False,
       )
       detections = []
       result = results[0]
       if result.boxes is None:
           return detections
       for box in result.boxes:
           cls = int(box.cls.item())
           confidence = float(box.conf.item())

           x_center, y_center, width, height = (
            box.xywhn[0].tolist()
           )

           detections.append({
            "class_id": cls,
            "confidence": confidence,
            "x_center": x_center,
            "y_center": y_center,
            "width": width,
            "height": height,
           })
       return detections
