import random
import shutil
from pathlib import Path
from app.services.dataset.config import (
   SELECTED_FRAMES_DIR,
   SEED_DATASET_DIR,
   SEED_DATASET_SIZE,
   RANDOM_SEED,
)

class SeedDatasetSelector:
   def __init__(self):
       random.seed(RANDOM_SEED)
       self.source = SELECTED_FRAMES_DIR
       self.destination = SEED_DATASET_DIR
   def build(self):
       print("\n" + "=" * 60)
       print("BUILDING SEED DATASET")
       print("=" * 60)
       image_extensions = {
           ".jpg",
           ".jpeg",
           ".png"
       }
       images = []
       for image in self.source.rglob("*"):
           if image.suffix.lower() in image_extensions:
               images.append(image)
       print(f"Available Images : {len(images)}")
       random.shuffle(images)
       selected = images[:min(SEED_DATASET_SIZE, len(images))]
       print(f"Selected Images  : {len(selected)}")
       self.copy_images(selected)
       print("\n✓ Seed Dataset Created")
       return selected
   def copy_images(self, images):
       if self.destination.exists():
           shutil.rmtree(self.destination)
       self.destination.mkdir(
           parents=True,
           exist_ok=True
       )
       for image in images:
           relative_path = image.relative_to(self.source)
           destination = (
               self.destination /
               relative_path
           )
           destination.parent.mkdir(
               parents=True,
               exist_ok=True
           )
           shutil.copy2(
               image,
               destination
           )

