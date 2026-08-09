from pathlib import Path
from app.services.dataset.frame_scanner import FrameScanner

RAW_FRAMES = Path("dataset/raw_frames")

def main():
   scanner = FrameScanner(RAW_FRAMES)
   dataset = scanner.scan()
   print("=" * 60)
   print("DATASET SUMMARY")
   print("=" * 60)
   print(f"Total Cameras : {dataset.total_cameras}")
   print(f"Total Videos  : {dataset.total_videos}")
   print(f"Total Frames  : {dataset.extracted_frames}")
   print()
   for camera in dataset.cameras:
       print(f"Camera : {camera.camera_name}")
       print(f"Videos : {camera.total_videos}")
       print(f"Frames : {camera.extracted_frames}")
       for video in camera.videos:
           print(
               f"   {video.video_name} "
               f"({video.extracted_frames} frames)"
           )
       print()

if __name__ == "__main__":
   main()
