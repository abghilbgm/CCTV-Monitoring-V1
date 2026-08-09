"""
Central class definitions used by the annotation engine.
These IDs must remain consistent with the YOLO training dataset.
"""
PPE_CLASSES = {
   0: "helmet",
   1: "no_helmet",
   2: "safety_vest",
   3: "no_safety_vest",
   4: "safety_shoes",
   5: "no_safety_shoes",
   6: "person"
}
CLASS_TO_ID = {
   name: idx
   for idx, name in PPE_CLASSES.items()
}
