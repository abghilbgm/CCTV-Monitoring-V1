from pathlib import Path
import cv2
from tqdm import tqdm

from app.core.settings import (
    VIDEO_ROOT,
    FRAME_OUTPUT,
    METADATA_OUTPUT,
    FRAME_INTERVAL,
    IMAGE_FORMAT,
)

from app.services.frame_extractor.video_reader import VideoReader
from app.services.frame_extractor.output_manager import OutputManager
from app.services.frame_extractor.metadata import MetadataManager
from app.services.frame_extractor.duplicate_filter import DuplicateFilter


class FrameExtractor:

    def __init__(self):
        self.output_manager = OutputManager(FRAME_OUTPUT)
        self.metadata = MetadataManager(METADATA_OUTPUT)
        self.filter = DuplicateFilter()

    def process_all_cameras(self):

        if not VIDEO_ROOT.exists():
            raise FileNotFoundError(
                f"Video folder not found:\n{VIDEO_ROOT}"
            )

        camera_folders = [
            folder
            for folder in VIDEO_ROOT.iterdir()
            if folder.is_dir()
        ]

        print(f"\nFound {len(camera_folders)} camera folders.\n")

        for camera_folder in camera_folders:
            self.process_camera(camera_folder)

        print("\nFrame extraction completed successfully.")

    def process_camera(self, camera_folder: Path):

        camera_name = camera_folder.name

        print(f"\nProcessing Camera : {camera_name}")

        video_files = sorted(
            camera_folder.glob("*.mp4")
        )

        print(f"Videos Found : {len(video_files)}")

        for video in video_files:
            self.process_video(camera_name, video)

    def process_video(self, camera_name, video_path):

        video_name = video_path.stem

        output_folder = (
            self.output_manager.create_video_output_folder(
                camera_name,
                video_name,
            )
        )

        # Check if frames already exist
        existing_frames = list(
            output_folder.glob(f"*.{IMAGE_FORMAT}")
        )

        if len(existing_frames) > 0:
            print(
                f"Skipping already processed video: "
                f"{video_name} "
                f"({len(existing_frames)} frames found)"
            )
            return

        print(f"\nProcessing Video : {video_name}")

        reader = VideoReader(video_path)

        capture = reader.open()

        fps = reader.get_fps()
        total_frames = reader.get_total_frames()

        progress = tqdm(
            total=total_frames,
            desc=video_name,
            unit="frame"
        )

        frame_number = 0
        saved_frames = 0

        while True:

            success, frame = capture.read()

            if not success:
                break

            if frame_number % FRAME_INTERVAL == 0:

                if self.filter.should_save():

                    image_name = (
                        f"frame_{saved_frames:06d}.{IMAGE_FORMAT}"
                    )

                    image_path = output_folder / image_name

                    # Extra protection against duplicates
                    if not image_path.exists():

                        cv2.imwrite(
                            str(image_path),
                            frame
                        )

                        timestamp = (
                            frame_number / fps
                            if fps > 0
                            else 0
                        )

                        self.metadata.save(
                            camera_name,
                            video_name,
                            frame_number,
                            round(timestamp, 2),
                            str(image_path),
                        )

                        saved_frames += 1
            frame_number += 1
            progress.update(1)

        progress.close()

        reader.release()

        print(
            f"Saved {saved_frames} frames from {video_name}"
        )


if __name__ == "__main__":
    extractor = FrameExtractor()
    extractor.process_all_cameras()
