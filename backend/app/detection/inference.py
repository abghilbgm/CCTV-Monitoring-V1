import cv2
from pathlib import Path
from detector import PPEDetector
from association import PPEAssociation
from violation_checker import ViolationChecker
from visualizer import Visualizer

class PPEInference:
   def __init__(self):
       self.detector = PPEDetector()
       self.association = PPEAssociation()
       self.checker = ViolationChecker()
       self.visualizer = Visualizer()
       self.project_root = Path(__file__).resolve().parents[2]
   ###########################################################
   def run_image(self, image_path):
       frame = cv2.imread(str(image_path))
       if frame is None:
           print(f"Unable to read image : {image_path}")
           return None
       results = self.detector.detect(frame)
       result = results[0]
       detections = []
       for box in result.boxes:
           cls = int(box.cls.item())
           x1, y1, x2, y2 = map(int, box.xyxy[0])
           detections.append({
               "class": cls,
               "box": (x1, y1, x2, y2)
           })
       # -----------------------------
       # Process each detected person
       # -----------------------------
       for det in detections:
           if det["class"] != 6:
               continue
           person_box = det["box"]
           ppe = self.association.associate(
               person_box,
               detections
           )
           status = self.checker.evaluate_person(
               ppe["has_helmet"],
               ppe["has_vest"],
               ppe["has_shoes"],
               ppe["has_no_helmet"],
               ppe["has_no_vest"],
               ppe["has_no_shoes"]
           )
           frame = self.visualizer.draw_person(
               frame,
               person_box,
               status["status"]
           )
       return frame
   ###########################################################
   def run_folder(self, input_folder, output_folder):
       input_folder = Path(input_folder)
       output_folder = Path(output_folder)
       image_extensions = {".jpg", ".jpeg", ".png"}
       total_images = 0
       for image_path in input_folder.rglob("*"):
           if image_path.suffix.lower() not in image_extensions:
               continue
           print(f"Processing : {image_path.relative_to(input_folder)}")
           frame = self.run_image(image_path)
           if frame is None:
               continue
           save_path = output_folder / image_path.relative_to(input_folder)
           save_path.parent.mkdir(
               parents=True,
               exist_ok=True
           )
           cv2.imwrite(str(save_path), frame)
           total_images += 1
       print("\n====================================")
       print("Inference Completed")
       print(f"Images Processed : {total_images}")
       print(f"Output Folder    : {output_folder}")
       print("====================================")

##############################################################
if __name__ == "__main__":
   project_root = Path(__file__).resolve().parents[2]
   input_folder = (
       project_root
       / "dataset"
       / "selected_frames"
   )
   output_folder = (
       project_root
       / "dataset"
       / "inference_output"
   )
   app = PPEInference()
   app.run_folder(
       input_folder,
       output_folder
   )
