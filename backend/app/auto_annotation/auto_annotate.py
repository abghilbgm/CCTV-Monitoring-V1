from ultralytics import YOLO
from pathlib import Path
import shutil
import yaml

# -------------------------------------------------------
# Project paths
# -------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "runs" / "ppe_detector" / "weights" / "best.pt"

SOURCE = PROJECT_ROOT / "dataset" / "selected_frames"

OUTPUT = PROJECT_ROOT / "dataset" / "auto_annotations"

# -------------------------------------------------------
# Dataset folders
# -------------------------------------------------------
IMAGES_DIR = OUTPUT / "images" / "train"
LABELS_DIR = OUTPUT / "labels" / "train"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LABELS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------
# Verify paths
# -------------------------------------------------------
print(f"Model Path : {MODEL_PATH}")
print(f"Source Path: {SOURCE}")

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not SOURCE.exists():
    raise FileNotFoundError(f"Source folder not found: {SOURCE}")

# -------------------------------------------------------
# Find all images recursively
# -------------------------------------------------------
image_files = sorted(
    list(SOURCE.rglob("*.jpg")) +
    list(SOURCE.rglob("*.jpeg")) +
    list(SOURCE.rglob("*.png"))
)

print(f"\nFound {len(image_files)} images")

if len(image_files) == 0:
    raise Exception("No images found!")

# -------------------------------------------------------
# Load model
# -------------------------------------------------------
model = YOLO(str(MODEL_PATH))

print("\nRunning auto annotation...")

# -------------------------------------------------------
# Predict image-by-image
# -------------------------------------------------------
for idx, img_path in enumerate(image_files, start=1):

    results = model.predict(
        source=str(img_path),
        save=False,
        verbose=False,
        conf=0.40
    )

    result = results[0]

    # Copy image
    shutil.copy2(
        img_path,
        IMAGES_DIR / img_path.name
    )

    # Label file
    label_path = LABELS_DIR / f"{img_path.stem}.txt"

    with open(label_path, "w") as f:

        if result.boxes is not None:

            for box in result.boxes:

                cls = int(box.cls.item())

                x, y, w, h = box.xywhn[0].tolist()

                f.write(
                    f"{cls} "
                    f"{x:.6f} "
                    f"{y:.6f} "
                    f"{w:.6f} "
                    f"{h:.6f}\n"
                )

    if idx % 100 == 0:
        print(f"Processed {idx}/{len(image_files)} images")

# -------------------------------------------------------
# Create data.yaml
# -------------------------------------------------------
data = {
    "path": ".",
    "train": "images/train",
    "val": "images/train",
    "names": {
        0: "helmet",
        1: "no_helmet",
        2: "safety_vest",
        3: "no_safety_vest",
        4: "safety_shoes",
        5: "no_safety_shoes",
        6: "person"
    }
}

with open(OUTPUT / "data.yaml", "w") as f:
    yaml.dump(data, f, sort_keys=False)

print("\n✅ Auto annotation completed successfully!")
print(f"Total Images Processed: {len(image_files)}")
print(f"Dataset Saved At: {OUTPUT}")
