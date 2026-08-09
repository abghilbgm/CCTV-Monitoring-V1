from app.services.dataset.models import DatasetSummary
from app.services.dataset.config import TOTAL_LABEL_IMAGES

class DatasetRecommender:
   def recommend(self, dataset: DatasetSummary):
       total_activity = sum(
           camera.activity_score
           for camera in dataset.cameras
       )
       if total_activity == 0:
           return dataset
    #    TOTAL_LABEL_IMAGES = 3000
       for camera in dataset.cameras:
           camera.labeling_priority = (
               camera.activity_score /
               total_activity
           )
           camera.frames_to_label = int(
               camera.labeling_priority *
               TOTAL_LABEL_IMAGES
           )
           for video in camera.videos:
               if camera.activity_score > 0:
                   video.label_priority = (
                       video.activity_score /
                       camera.activity_score
                   )
                   video.recommended_frames = int(
                       video.label_priority *
                       camera.frames_to_label
                   )
                   video.recommended_for_labeling = (
                       video.recommended_frames > 0
                   )
       return dataset
