from dataclasses import dataclass

@dataclass
class AnnotationStatistics:
   images_processed: int = 0
   images_with_detections: int = 0
   images_without_detections: int = 0
   total_objects: int = 0
   total_labels_written: int = 0
