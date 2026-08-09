from pathlib import Path

# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(".")

DATASET_ROOT = PROJECT_ROOT / "dataset"

RAW_FRAMES_DIR = DATASET_ROOT / "raw_frames"
SELECTED_FRAMES_DIR = DATASET_ROOT / "selected_frames"
# ANNOTATED_DATASET_DIR = DATASET_ROOT / "annotated_dataset"
ANNOTATIONS_DIR = DATASET_ROOT / "annotations"
FINAL_DATASET_DIR = DATASET_ROOT / "final_dataset"
SEED_DATASET_DIR = DATASET_ROOT / "seed_dataset"
IMAGES_DIR = FINAL_DATASET_DIR / "images"
LABELS_DIR = FINAL_DATASET_DIR / "labels"

# ==========================================================
# CVAT EXPORT
# ==========================================================
CVAT_EXPORT_DIR = DATASET_ROOT / "task_dataset" / "obj_train_data" / "seed_dataset"

# ==========================================================
# FINAL DATASET
# ==========================================================
TRAIN_IMAGES_DIR = FINAL_DATASET_DIR / "images" / "train"
VAL_IMAGES_DIR = FINAL_DATASET_DIR / "images" / "val"
TEST_IMAGES_DIR = FINAL_DATASET_DIR / "images" / "test"

TRAIN_LABELS_DIR = FINAL_DATASET_DIR / "labels" / "train"
VAL_LABELS_DIR = FINAL_DATASET_DIR / "labels" / "val"
TEST_LABELS_DIR = FINAL_DATASET_DIR / "labels" / "test"

# ==========================================================
# MODEL PATHS
# ==========================================================

MODEL_ROOT = PROJECT_ROOT / "app" / "models"

PERSON_MODEL = MODEL_ROOT / "yolov8n.pt"
PPE_MODEL = MODEL_ROOT / "yolov8n.pt"

# ==========================================================
# DATASET SETTINGS
# ==========================================================

TOTAL_LABEL_IMAGES = 3000
IMAGE_SIZE = 640
PERSON_CONFIDENCE = 0.35
PPE_CONFIDENCE = 0.25

# ==========================================================
# YOLO DATASET SPLIT
# ==========================================================

TRAIN_SPLIT = 0.80
VAL_SPLIT = 0.10
TEST_SPLIT = 0.10

# ==========================================================
# RANDOMNESS
# ==========================================================

RANDOM_SEED = 42

# ==========================================================
# SEED DATASET
# ==========================================================
SEED_DATASET_SIZE = 500
