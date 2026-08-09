class ViolationChecker:
   def evaluate_person(
       self,
       has_helmet,
       has_vest,
       has_shoes,
       has_no_helmet,
       has_no_vest,
       has_no_shoes,
   ):
       violations = []
       # Highest priority
       if has_no_helmet:
           violations.append("Helmet")
       if has_no_vest:
           violations.append("Safety Vest")
       # Helmet must be present
       if not has_helmet:
           violations.append("Helmet Not Detected")
       # Vest must be present
       if not has_vest:
           violations.append("Safety Vest Not Detected")
       # Shoes are ignored for red/green status
       # We still receive has_shoes and has_no_shoes
       # so we can use them later for reports.
       if len(violations) == 0:
           return {
               "status": "SAFE",
               "color": "green",
               "violations": []
           }
       return {
           "status": "VIOLATION",
           "color": "red",
           "violations": violations
       }
