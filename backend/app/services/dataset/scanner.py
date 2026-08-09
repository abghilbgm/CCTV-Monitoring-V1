from pathlib import Path
from app.core.settings import VIDEO_ROOT
from app.services.dataset.models import (
    CameraStatistics,
    VideoStatistics,
)


class DatasetScanner:
    def __init__(self):

        self.video_root = VIDEO_ROOT

    def scan(self):

        cameras = []

        for camera_folder in sorted(self.video_root.iterdir()):

            if not camera_folder.is_dir():

                continue

            camera = CameraStatistics(

                camera_name=camera_folder.name

            )

            mp4_files = sorted(

                camera_folder.glob("*.mp4")

            )

            camera.total_videos = len(mp4_files)

            for video in mp4_files:

                stats = VideoStatistics(

                    camera_name=camera_folder.name,

                    video_name=video.stem,

                    video_path=video

                )

                camera.videos.append(stats)

            cameras.append(camera)

        return cameras
 
