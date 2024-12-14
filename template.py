from pydantic import BaseModel
from typing import List, Optional

class WeeklyUpdate(BaseModel):
    summary: Optional[List[str]] = []  # List of points under "Summary"
    progress: Optional[List[str]] = []  # List of points under "Progress"
    roadblocks: Optional[List[str]] = []  # List of points under "Roadblocks"
    next_week_work: Optional[List[str]] = []  # List of points under "Next Week's Work"
    next_week_work_location: Optional[List[str]] = []  # List of work locations for next week

raw_template =  """

### 1. Summary  
-  

### 2. Progress  
-  

### 3. Roadblocks  
-  

### 4. Next Week's Work  
-  

### 5. Work Location (Next Week)  
-  """