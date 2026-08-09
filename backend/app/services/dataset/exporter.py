import shutil
from pathlib import Path

from app.services.dataset.config import FINAL_DATASET_DIR


class DatasetExporter:
    def __init__(self):
        self.dataset_root = FINAL_DATASET_DIR

    def export(self, dataset_split: dict):
        self.create_directories()

        for split_name, images in dataset_split.items():
            image_output = (
                self.dataset_root
                / "images"
                / split_name
            )

            label_output = (
                self.dataset_root
                / "labels"
                / split_name
            )

            for image_path in images:
                relative_parts = image_path.relative_to(
                    image_path.parents[2]
                ).parts

                unique_name = "_".join(relative_parts)

                destination_image = (
                    image_output
                    / unique_name
                )

                shutil.copy2(
                    image_path,
                    destination_image
                )

                label_path = image_path.with_suffix(".txt")

                if label_path.exists():
                    destination_label = (
                        label_output
                        / destination_image.with_suffix(".txt").name
                    )

                    shutil.copy2(
                        label_path,
                        destination_label
                    )

    def create_directories(self):
        for split in [
            "train",
            "val",
            "test"
        ]:
            (
                self.dataset_root
                / "images"
                / split
            ).mkdir(
                parents=True,
                exist_ok=True
            )

            (
                self.dataset_root
                / "labels"
                / split
            ).mkdir(
                parents=True,
                exist_ok=True
            )
