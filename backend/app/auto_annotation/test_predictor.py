from ultralytics import YOLO
from pathlib import Path
import cv2
model = YOLO("../../runs/ppe_detector/weights/best.pt")
image = (
   Path(__file__).resolve().parents[2]
   / "dataset"
   / "selected_frames"
   / "cam 2 30.6.26"
   / "D02_20260630111410"
   / "frame_000060.jpg"
)
results = model(str(image))
class_names = {
   0: "Helmet",
   1: "No Helmet",
   2: "Safety Vest",
   3: "No Safety Vest",
   4: "Safety Shoes",
   5: "No Safety Shoes",
   6: "Person"
}
print("\nDetected Objects\n")
for box in results[0].boxes:
   cls = int(box.cls[0])
   conf = float(box.conf[0])
   print(f"{class_names[cls]} : {conf:.2f}")
annotated = results[0].plot()
cv2.imshow("Prediction", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
