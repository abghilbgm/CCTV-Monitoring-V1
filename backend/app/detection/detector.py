from pathlib import Path
from ultralytics import YOLO

class PPEDetector:
   def __init__(self):
       self.project_root = Path(__file__).resolve().parents[2]
       self.model_path = (
           self.project_root
           / "runs"
           / "ppe_detector"
           / "weights"
           / "best.pt"
       )
       print(f"Loading model:\n{self.model_path}")
       self.model = YOLO(str(self.model_path))
       print("✅ PPE Model Loaded Successfully!")
   def detect(self, frame, confidence=0.50):
       return self.model.predict(
           source=frame,
           conf=confidence,
           verbose=False
       )
