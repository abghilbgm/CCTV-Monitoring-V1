from ultralytics import YOLO
from pathlib import Path
import cv2

# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "runs"
    / "ppe_detector"
    / "weights"
    / "best.pt"
)

INPUT_FOLDER = (
    PROJECT_ROOT
    / "dataset"
    / "final_dataset"
    / "images"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "runs"
    / "predictions"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load model
# --------------------------------------------------

print(f"Loading model: {MODEL_PATH}")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found:\n{MODEL_PATH}"
    )

model = YOLO(str(MODEL_PATH))

# --------------------------------------------------
# Find images
# --------------------------------------------------

print(f"Input folder: {INPUT_FOLDER}")
print(f"Folder exists: {INPUT_FOLDER.exists()}")

images = list(INPUT_FOLDER.rglob("*.jpg"))

print(f"Found {len(images)} images")

if len(images) == 0:
    raise ValueError(
        f"No JPG images found in:\n{INPUT_FOLDER}"
    )

# --------------------------------------------------
# Run inference
# --------------------------------------------------

for i, img_path in enumerate(images, start=1):

    print(
        f"[{i}/{len(images)}] Processing: {img_path.name}"
    )

    results = model(str(img_path))

    annotated_image = results[0].plot()

    output_path = OUTPUT_FOLDER / img_path.name

    cv2.imwrite(
        str(output_path),
        annotated_image
    )

# --------------------------------------------------
# Done
# --------------------------------------------------

print("\n✅ Inference completed successfully!")
print(f"✅ Results saved to:\n{OUTPUT_FOLDER}")
