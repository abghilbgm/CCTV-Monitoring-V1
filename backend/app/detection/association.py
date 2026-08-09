class PPEAssociation:
   def __init__(self):
       pass
   ####################################################
   def center_inside(self, zone_box, object_box):
       zx1, zy1, zx2, zy2 = zone_box
       ox1, oy1, ox2, oy2 = object_box
       cx = (ox1 + ox2) / 2
       cy = (oy1 + oy2) / 2
       return (
           zx1 <= cx <= zx2 and
           zy1 <= cy <= zy2
       )
   ####################################################
   def head_zone(self, person_box):
       x1, y1, x2, y2 = person_box
       h = y2 - y1
       return (
           x1,
           y1,
           x2,
           y1 + int(h * 0.35)
       )
   ####################################################
   def torso_zone(self, person_box):
       x1, y1, x2, y2 = person_box
       h = y2 - y1
       return (
           x1,
           y1 + int(h * 0.25),
           x2,
           y1 + int(h * 0.75)
       )
   ####################################################
   def feet_zone(self, person_box):
       x1, y1, x2, y2 = person_box
       h = y2 - y1
       return (
           x1,
           y2 - int(h * 0.25),
           x2,
           y2
       )
   ####################################################
   def associate(self, person_box, detections):
       head = self.head_zone(person_box)
       torso = self.torso_zone(person_box)
       feet = self.feet_zone(person_box)
       result = {
           "has_helmet": False,
           "has_vest": False,
           "has_shoes": False,
           "has_no_helmet": False,
           "has_no_vest": False,
           "has_no_shoes": False
       }
       for det in detections:
           cls = det["class"]
           box = det["box"]
           # Ignore person detections
           if cls == 6:
               continue
           # Helmet
           if cls == 0 and self.center_inside(head, box):
               result["has_helmet"] = True
           elif cls == 1 and self.center_inside(head, box):
               result["has_no_helmet"] = True
           # Vest
           elif cls == 2 and self.center_inside(torso, box):
               result["has_vest"] = True
           elif cls == 3 and self.center_inside(torso, box):
               result["has_no_vest"] = True
           # Shoes
           elif cls == 4 and self.center_inside(feet, box):
               result["has_shoes"] = True
           elif cls == 5 and self.center_inside(feet, box):
               result["has_no_shoes"] = True
       return result
