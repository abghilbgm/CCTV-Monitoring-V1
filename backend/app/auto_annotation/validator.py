from pathlib import Path
from collections import Counter

class DatasetValidator:
   def __init__(self):
       self.project_root = Path(__file__).resolve().parents[2]
       self.labels_dir = (
           self.project_root
           / "dataset"
           / "auto_annotations"
           / "labels"
           / "train"
       )
       self.class_names = {
           0: "helmet",
           1: "no_helmet",
           2: "safety_vest",
           3: "no_safety_vest",
           4: "safety_shoes",
           5: "no_safety_shoes",
           6: "person",
       }
   def validate(self):
       label_files = list(self.labels_dir.glob("*.txt"))
       total_images = len(label_files)
       empty_files = 0
       class_counter = Counter()
       for file in label_files:
           lines = file.read_text().strip().splitlines()
           if not lines:
               empty_files += 1
               continue
           for line in lines:
               cls = int(line.split()[0])
               class_counter[cls] += 1
       print("\n========== DATASET SUMMARY ==========\n")
       print(f"Label files           : {total_images}")
       print(f"Empty label files     : {empty_files}")
       print("\nObjects detected:\n")
       for cls_id in sorted(self.class_names.keys()):
           print(
               f"{self.class_names[cls_id]:18}"
               f": {class_counter[cls_id]}"
           )

if __name__ == "__main__":
   validator = DatasetValidator()
   validator.validate()
