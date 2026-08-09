import shutil
from pathlib import Path
from app.services.dataset.config import (
   SELECTED_FRAMES_DIR,
   ANNOTATIONS_DIR,
)
from app.services.dataset.annotator.detector import Detector
from app.services.dataset.annotator.label_writer import LabelWriter
from app.services.dataset.annotator.statistics import (
   AnnotationStatistics,
)

class AutoAnnotator:
   def __init__(self):
       self.detector = Detector()
       self.statistics = AnnotationStatistics()
   def annotate(self):
       print("\n" + "=" * 60)
       print("AUTO ANNOTATION")
       print("=" * 60)
       image_extensions = {".jpg", ".jpeg", ".png"}
       for image_path in sorted(
           SELECTED_FRAMES_DIR.rglob("*")
       ):
           if image_path.suffix.lower() not in image_extensions:
               continue
           relative_path = image_path.relative_to(
               SELECTED_FRAMES_DIR
           )
           destination_image = (
               ANNOTATIONS_DIR / relative_path
           )
           destination_image.parent.mkdir(
               parents=True,
               exist_ok=True,
           )
           shutil.copy2(
               image_path,
               destination_image,
           )
           detections = self.detector.detect(
               destination_image
           )
           LabelWriter.write(
               destination_image,
               detections,
           )
           self.statistics.images_processed += 1
           if detections:
               self.statistics.images_with_detections += 1
               self.statistics.total_objects += len(
                   detections
               )
               self.statistics.total_labels_written += len(
                   detections
               )
           else:
               self.statistics.images_without_detections += 1
       self.print_summary()
       return self.statistics
   def print_summary(self):
       print("\n" + "=" * 60)
       print("ANNOTATION SUMMARY")
       print("=" * 60)
       print(
           f"Images Processed      : "
           f"{self.statistics.images_processed}"
       )
       print(
           f"Images With Objects   : "
           f"{self.statistics.images_with_detections}"
       )
       print(
           f"Images Without Objects: "
           f"{self.statistics.images_without_detections}"
       )
       print(
           f"Objects Detected      : "
           f"{self.statistics.total_objects}"
       )
       print(
           f"Labels Written        : "
           f"{self.statistics.total_labels_written}"
       )
       print("=" * 60)
