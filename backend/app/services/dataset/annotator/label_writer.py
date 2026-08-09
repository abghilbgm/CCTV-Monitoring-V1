from pathlib import Path

class LabelWriter:
   @staticmethod
   def write(image_path: Path, detections: list):
       label_path = image_path.with_suffix(".txt")
       lines = []
       for detection in detections:
           class_id = detection["class_id"]
           x_center = detection["x_center"]
           y_center = detection["y_center"]
           width = detection["width"]
           height = detection["height"]
           lines.append(
               f"{class_id} "
               f"{x_center:.6f} "
               f"{y_center:.6f} "
               f"{width:.6f} "
               f"{height:.6f}"
           )
       with open(label_path, "w") as f:
           f.write("\n".join(lines))
