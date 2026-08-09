from pathlib import Path
from app.services.dataset.frame_scanner import FrameScanner
from app.services.dataset.analyzer import DatasetAnalyzer
RAW_FRAMES = Path("dataset/raw_frames")
MODEL_PATH = "backend/app/models/yolov8n.pt"

def main():
   # Scan the extracted frames
   scanner = FrameScanner(RAW_FRAMES)
   dataset = scanner.scan()
   # Keep only ONE camera and ONE video for testing
   dataset.cameras = dataset.cameras[:1]
   dataset.cameras[0].videos = dataset.cameras[0].videos[:1]
   analyzer = DatasetAnalyzer(MODEL_PATH)
   dataset = analyzer.analyze(dataset)
   camera = dataset.cameras[0]
   video = camera.videos[0]
   print("\n" + "=" * 60)
   print("ANALYSIS RESULT")
   print("=" * 60)
   print(f"Camera              : {camera.camera_name}")
   print(f"Video               : {video.video_name}")
   print(f"Extracted Frames    : {video.extracted_frames}")
   print(f"Frames With Persons : {video.person_frames}")
   print(f"Total Persons       : {video.total_persons}")
   print(f"Maximum Persons     : {video.max_persons_in_frame}")
   print(f"Activity Score      : {video.activity_score:.4f}")

if __name__ == "__main__":
   main()

