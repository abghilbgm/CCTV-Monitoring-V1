from scanner import DatasetScanner
from analyzer import DatasetAnalyzer
from recommender import DatasetRecommender
from selector import DatasetSelector

RAW_FRAMES = "dataset/raw_frames"
SELECTED_FRAMES = "backend/dataset/selected_frames"

def main():
   print("=" * 60)
   print("PPE DATASET PIPELINE")
   print("=" * 60)
   # Step 1
   print("\n[1] Scanning dataset...")
   scanner = DatasetScanner(RAW_FRAMES)
   dataset = scanner.scan()
   # Step 2
   print("\n[2] Analyzing dataset...")
   analyzer = DatasetAnalyzer()
   dataset = analyzer.analyze(dataset)
   # Step 3
   print("\n[3] Recommending frames...")
   recommender = DatasetRecommender()
   dataset = recommender.recommend(dataset)
   # Step 4
   print("\n[4] Selecting frames...")
   selector = DatasetSelector(
       output_directory=SELECTED_FRAMES
   )
   selector.select(dataset)
   print("\nPipeline Completed Successfully!")

if __name__ == "__main__":
   main()
