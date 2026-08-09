from ultralytics import YOLO
from pathlib import Path

class PPETrainer:
   def __init__(self):
       self.project_root = Path(__file__).resolve().parents[2]
       # Auto-annotated dataset
       self.dataset_yaml = (
           self.project_root
           / "dataset"
           / "auto_annotations"
           / "data.yaml"
       )
       # Start training from the pretrained YOLOv8 Nano model
       self.model = YOLO("yolov8n.pt")
   def train(self):
       print("=" * 60)
       print("Starting PPE Model Training")
       print("=" * 60)
       print(f"Dataset : {self.dataset_yaml}")
       print()
       self.model.train(
           data=str(self.dataset_yaml),
           # Training parameters
           epochs=100,
           imgsz=640,
           batch=8,
           # CPU training
           workers=2,
           device="cpu",
           # Output
           project=str(self.project_root / "runs"),
           name="ppe_detector",
           exist_ok=True,
           # Training options
           pretrained=True,
           optimizer="AdamW",
           patience=20,
           cache=True,
           plots=True,
           save=True,
           verbose=True
       )
       print("\nTraining Completed Successfully!")
       print("\nBest Model:")
       print(
           self.project_root
           / "runs"
           / "ppe_detector"
           / "weights"
           / "best.pt"
       )

if __name__ == "__main__":
   trainer = PPETrainer()
   trainer.train()
