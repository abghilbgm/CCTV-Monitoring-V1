from app.services.dataset.seed_selector import SeedDatasetSelector

def main():
   selector = SeedDatasetSelector()
   selected_images = selector.build()
   print("\n" + "=" * 60)
   print("SEED DATASET SUMMARY")
   print("=" * 60)
   print(f"Total Selected Images : {len(selected_images)}")
   if selected_images:
       print("\nSample Images:")
       for image in selected_images[:10]:
           print(image)

if __name__ == "__main__":
   main()
