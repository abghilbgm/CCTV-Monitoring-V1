from dataclasses import dataclass, field
from pathlib import Path

from app.services.dataset.config import ANNOTATIONS_DIR
from app.services.dataset.annotator.classes import PPE_CLASSES


@dataclass
class ValidationReport:
    images: int = 0
    label_files: int = 0
    missing_labels: int = 0
    invalid_labels: int = 0
    invalid_class_ids: int = 0
    invalid_coordinates: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self):
        return (
            self.missing_labels == 0
            and self.invalid_labels == 0
            and self.invalid_class_ids == 0
            and self.invalid_coordinates == 0
        )


class DatasetValidator:
    def __init__(self):
        self.dataset_root = ANNOTATIONS_DIR
        self.valid_classes = set(PPE_CLASSES.keys())

    def validate(self):
        report = ValidationReport()

        image_extensions = {
            ".jpg",
            ".jpeg",
            ".png"
        }

        for image_path in sorted(self.dataset_root.rglob("*")):
            if image_path.suffix.lower() not in image_extensions:
                continue

            report.images += 1

            label_path = image_path.with_suffix(".txt")

            if not label_path.exists():
                report.missing_labels += 1
                report.errors.append(
                    f"Missing label: {label_path}"
                )
                continue

            report.label_files += 1

            self.validate_label_file(
                label_path,
                report
            )

        self.print_summary(report)

        return report

    def validate_label_file(
        self,
        label_path,
        report,
    ):
        lines = label_path.read_text().splitlines()

        for line in lines:
            if not line.strip():
                continue

            values = line.split()

            if len(values) != 5:
                report.invalid_labels += 1
                report.errors.append(
                    f"{label_path}: Invalid format"
                )
                continue

            class_id = int(values[0])

            if class_id not in self.valid_classes:
                report.invalid_class_ids += 1
                report.errors.append(
                    f"{label_path}: Invalid class {class_id}"
                )
                continue

            coordinates = list(
                map(float, values[1:])
            )

            x, y, w, h = coordinates

            if not (
                0 <= x <= 1
                and 0 <= y <= 1
                and 0 < w <= 1
                and 0 < h <= 1
            ):
                report.invalid_coordinates += 1
                report.errors.append(
                    f"{label_path}: Invalid coordinates"
                )

    def print_summary(self, report):
        print("\n" + "=" * 60)
        print("DATASET VALIDATION")
        print("=" * 60)

        print(f"Images               : {report.images}")
        print(f"Label Files          : {report.label_files}")
        print(f"Missing Labels       : {report.missing_labels}")
        print(f"Invalid Labels       : {report.invalid_labels}")
        print(f"Invalid Class IDs    : {report.invalid_class_ids}")
        print(f"Invalid Coordinates  : {report.invalid_coordinates}")
        print()

        if report.passed:
            print("✓ DATASET VALIDATION PASSED")
        else:
            print("✗ DATASET VALIDATION FAILED")
            print("\nErrors:")

            for error in report.errors[:10]:
                print(f" - {error}")

            if len(report.errors) > 10:
                print(
                    f"... {len(report.errors) - 10} more errors"
                )

        print("=" * 60)
