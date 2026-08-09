from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class VideoStatistics:
   camera_name: str
   video_name: str
   video_path: Path

   # Path to extracted frames for this video
   frame_directory: Path | None = None

   total_frames: int = 0
   fps: float = 0.0
   duration_seconds: float = 0.0
   resolution_width: int = 0
   resolution_height: int = 0

   extracted_frames: int = 0

   person_frames: int = 0
   total_persons: int = 0
   max_persons_in_frame: int = 0

   activity_score: float = 0.0

   # Recommender fields
   label_priority: float = 0.0
   recommended_frames: int = 0
   recommended_for_labeling: bool = False

@dataclass
class CameraStatistics:

    camera_name: str

    total_videos: int = 0
    total_frames: int = 0
    extracted_frames: int = 0

    person_frames: int = 0
    total_persons: int = 0
    max_persons: int = 0

    activity_score: float = 0.0

    recommended_images: int = 0

    # Recommender fields

    labeling_priority: float = 0.0
    frames_to_label: int = 0
    videos: list[VideoStatistics] = field(default_factory=list)
 

@dataclass
class DatasetSummary:
   total_cameras: int = 0
   total_videos: int = 0

   total_frames: int = 0
   extracted_frames: int = 0

   total_persons: int = 0
   
   cameras: list[CameraStatistics] = field(default_factory=list)

from dataclasses import dataclass
from pathlib import Path

@dataclass
class FrameMetadata:
   image_path: Path
   camera_name: str
   video_name: str
   frame_number: int
   person_count: int = 0
   priority_score: float = 0.0
   selected: bool = False
