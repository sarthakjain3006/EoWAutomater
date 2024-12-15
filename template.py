from pydantic import BaseModel, Field


class Progress(BaseModel):
    headline: str = Field(
        default="summarizing headline",
        description="A minimal headline that encapsulates the changes that follow",
    )
    changes: list[str] = Field(
        default=["change from commits"],
        description="all changes from commits in a list",
    )


class Roadblock(BaseModel):
    headline: str = Field(
        default="summarizing headline",
        description="A minimal headline that encapsulates the roadblocks",
    )
    changes: list[str] = Field(
        default=["change from commits"],
        description="all possible roadblocks explained in detail",
    )


class WeeklyUpdate(BaseModel):
    summary: str = Field(
        default="The focus of this week was",
        description="A concise summary for all the progress in the week",
    )
    progress: list[Progress] = Field(
        default=[Progress()],
        description="A list of headlines and the respective changes explained in detail from the commits",
    )  # List of points under "Progress"
    roadblocks: list[Roadblock] = Field(
        default=[Roadblock()],
        description="A list of headlines and the respective roadblocks",
    )
    next_week_work: list[str] = Field(
        default=["Possible work generating from this weeks commits"],
        description="This can be a gathered from the changes in the commits, and should usually contain possible optimization, security or testing changes",
    )


raw_template = """

### 1. Summary  
-  This week's focus was <-- insert summary --> 

### 2. Progress  

-  Title 1
    - change 1
    - change 2

### 3. Roadblocks  

- Title 1
    - roadblock 1
    - roadblock 2

### 4. Next Week's Work 

- Title 1
    - next steps for Progress Title 1
    - next steps for Progress Title 2

### 5. Work Location
< -- location if provided in input else "In person all week"
"""
