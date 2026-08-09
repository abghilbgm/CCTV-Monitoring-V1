import cv2
from colors import GREEN, RED

class Visualizer:
   def draw_person(self, frame, person_box, status):
       color = GREEN if status == "SAFE" else RED
       x1, y1, x2, y2 = person_box
       cv2.rectangle(
           frame,
           (x1, y1),
           (x2, y2),
           color,
           3
       )
       return frame
