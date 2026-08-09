from pathlib import Path
from app.services.dataset.annotator.classes import PPE_CLASSES
from app.services.dataset.config import FINAL_DATASET_DIR

class YAMLGenerator:
   def __init__(self):
       self.dataset_root = FINAL_DATASET_DIR
   def generate(self):
       yaml_path = self.dataset_root / "data.yaml"
       lines = [
           f"path: {self.dataset_root.resolve()}",
           "",
           "train: images/train",
           "val: images/val",
           "test: images/test",
           "",
           f"nc: {len(PPE_CLASSES)}",
           "names:"
       ]
       for class_id, class_name in PPE_CLASSES.items():
           lines.append(
               f"  {class_id}: {class_name}"
           )
       yaml_path.write_text(
           "\n".join(lines)
       )
       print(f"✓ data.yaml created: {yaml_path}")
