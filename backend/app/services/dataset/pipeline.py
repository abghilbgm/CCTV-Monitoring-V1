from app.services.dataset.config import (
    RAW_FRAMES_DIR,
    SELECTED_FRAMES_DIR,
    PERSON_MODEL,
)

from app.services.dataset.frame_scanner import FrameScanner
from app.services.dataset.analyzer import DatasetAnalyzer
from app.services.dataset.recommender import DatasetRecommender
from app.services.dataset.selector import DatasetSelector
from app.services.dataset.annotator.annotator import AutoAnnotator
from app.services.dataset.validator import DatasetValidator
from app.services.dataset.dataset_builder import DatasetBuilder
from app.services.dataset.seed_selector import SeedDatasetSelector


class DatasetPipeline:
    def __init__(self):
        self.raw_frames_dir = RAW_FRAMES_DIR
        self.selected_frames_dir = SELECTED_FRAMES_DIR
        self.model_path = PERSON_MODEL

    def run(self):
        print("=" * 70)
        print("PPE DATASET PREPARATION PIPELINE")
        print("=" * 70)

        # ---------------------------------------------------
        # Step 1 - Scan Extracted Frames
        # ---------------------------------------------------
        print("\n[1/6] Scanning extracted frames...")

        scanner = FrameScanner(self.raw_frames_dir)
        dataset = scanner.scan()

        print(f"✓ Cameras : {dataset.total_cameras}")
        print(f"✓ Videos  : {dataset.total_videos}")
        print(f"✓ Frames  : {dataset.extracted_frames}")

        # ---------------------------------------------------
        # Step 2 - Analyze Dataset
        # ---------------------------------------------------
        print("\n[2/6] Analyzing dataset...")

        analyzer = DatasetAnalyzer(self.model_path)
        dataset = analyzer.analyze(dataset)

        # ---------------------------------------------------
        # Step 3 - Recommend Frames
        # ---------------------------------------------------
        print("\n[3/6] Recommending frames...")

        recommender = DatasetRecommender()
        dataset = recommender.recommend(dataset)

        # ---------------------------------------------------
        # Step 4 - Select Frames
        # ---------------------------------------------------
        print("\n[4/6] Selecting frames...")

        selector = DatasetSelector(self.selected_frames_dir)
        selector.select(dataset)

        # ---------------------------------------------------
        # Step 5 - Auto Annotation
        # ---------------------------------------------------
        print("\n[5/6] Auto Annotating...")

        annotator = AutoAnnotator()
        annotator.annotate()

        # ---------------------------------------------------
        # Step 6 - Validation
        # ---------------------------------------------------
        print("\n[6/6] Validating dataset...")

        validator = DatasetValidator()
        report = validator.validate()

        if not report.passed:
            raise RuntimeError(
                "Dataset validation failed."
            )

        # ---------------------------------------------------
        # Step 6 - Dataset Builder
        # ---------------------------------------------------
        print*"\n[7/7] Building Training Dataset..."
        builder = DatasetBuilder()
        builder.build()

        print*"\n[8/8] Building Seed Dataset..."
        seed_selector = SeedDatasetSelector()
        seed_selector.build()

        print("\n" + "=" * 70)
        print("✓ DATASET PIPELINE COMPLETED")
        print("=" * 70)

        return dataset
