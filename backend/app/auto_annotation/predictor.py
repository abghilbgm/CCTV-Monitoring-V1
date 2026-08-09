from pathlib import Path
from ultralytics import YOLO

class AutoAnnotator:
   def __init__(self):
       self.project_root = Path(__file__).resolve().parents[2]
       self.model_path = (
           self.project_root
           / "runs"
           / "ppe_detector"
           / "weights"
           / "best.pt"
       )
       self.model = YOLO(str(self.model_path))
   def predict(self, image_path, conf=0.35):
       results = self.model.predict(
           source=str(image_path),
           conf=conf,
           verbose=False
       )
       return results[0]
