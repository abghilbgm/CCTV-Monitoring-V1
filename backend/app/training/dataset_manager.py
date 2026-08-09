from pathlib import Path
import shutil
import random


class DatasetManager:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]

        self.selected_frames = (
            self.project_root / "dataset" / "selected_frames"
        )

        self.annotations = (
            self.project_root
            / "dataset"
            / "annotations"
            / "labels"
        )

        self.final_dataset = (
            self.project_root
            / "dataset"
            / "final_dataset"
        )

        self.images_train = self.final_dataset / "images" / "train"
        self.images_val = self.final_dataset / "images" / "val"
        self.images_test = self.final_dataset / "images" / "test"

        self.labels_train = self.final_dataset / "labels" / "train"
        self.labels_val = self.final_dataset / "labels" / "val"
        self.labels_test = self.final_dataset / "labels" / "test"

        self.image_index = {}
        self.annotation_files = []
        self.matched_files = []

    def create_directories(self):
        folders = [
            self.images_train,
            self.images_val,
            self.images_test,
            self.labels_train,
            self.labels_val,
            self.labels_test,
        ]

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

        print("✓ Dataset folders ready")

    def scan_images(self):
        print("\nScanning images...")

        count = 0

        for img in self.selected_frames.rglob("*.jpg"):
            key = img.relative_to(self.selected_frames)
            self.image_index[str(key)] = img
            count += 1

        print(f"✓ Indexed {count} images")

    def scan_annotations(self):
        print("\nScanning annotations...")

        self.annotation_files = list(
            self.annotations.rglob("*.txt")
        )

        print(f"✓ Found {len(self.annotation_files)} annotations")

    def match_files(self):
        print("\nMatching images with annotations...")

        matched = []
        missing = []

        for label in self.annotation_files:
            relative = label.relative_to(self.annotations)

            # Remove train/seed_dataset from path
            relative = Path(*relative.parts[2:])

            # Replace .txt with .jpg
            image_relative = relative.with_suffix(".jpg")

            image_path = self.selected_frames / image_relative

            if image_path.exists():
                matched.append((image_path, label))
            else:
                missing.append(image_relative)

        print(f"✓ Matched : {len(matched)}")
        print(f"✗ Missing : {len(missing)}")

        if missing:
            print("\nFirst few missing files:")
            for item in missing[:10]:
                print(item)

        self.matched_files = matched

    def copy_dataset(self):
        print("\nCopying matched files...")

        random.seed(42)

        files = self.matched_files.copy()
        random.shuffle(files)

        total = len(files)

        train_end = int(total * 0.8)
        val_end = int(total * 0.9)

        train = files[:train_end]
        val = files[train_end:val_end]
        test = files[val_end:]

        def copy_split(split, image_folder, label_folder):
            for image, label in split:
                shutil.copy2(
                    image,
                    image_folder / image.name
                )

                shutil.copy2(
                    label,
                    label_folder / label.name
                )

        copy_split(
            train,
            self.images_train,
            self.labels_train
        )

        copy_split(
            val,
            self.images_val,
            self.labels_val
        )

        copy_split(
            test,
            self.images_test,
            self.labels_test
        )

        print("\nDataset created successfully!")
        print(f"Train      : {len(train)}")
        print(f"Validation : {len(val)}")
        print(f"Test       : {len(test)}")

    def generate_yaml(self):
        yaml_text = f"""
path: {self.final_dataset.as_posix()}
train: images/train
val: images/val
test: images/test

names:
  0: helmet
  1: no_helmet
  2: safety_vest
  3: no_safety_vest
  4: safety_shoes
  5: no_safety_shoes
  6: person
"""

        yaml_path = self.final_dataset / "data.yaml"

        with open(yaml_path, "w") as f:
            f.write(yaml_text.strip())

        print(f"\n✓ data.yaml created at:\n{yaml_path}")


if __name__ == "__main__":
    manager = DatasetManager()

    manager.create_directories()
    manager.scan_images()
    manager.scan_annotations()
    manager.match_files()
    manager.copy_dataset()
    manager.generate_yaml()
