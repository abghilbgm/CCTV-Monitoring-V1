from app.services.frame_extractor.extractor import FrameExtractor

if __name__ == "__main__":
   extractor = FrameExtractor()
   extractor.process_all_cameras()
