from pydantic_ai import Agent
from dataclasses import dataclass, field
from changes.gitchanges import GitChanges
from pydantic import BaseModel, Field
from pydantic_ai import RunContext
from template import WeeklyUpdate

@dataclass
class SupportDependencies:  
    changes: GitChanges = GitChanges()
    template: dict = field(default_factory=WeeklyUpdate().model_dump)

class SupportResult(BaseModel):  

    report: WeeklyUpdate = Field(description="report")
    importance: bool = Field(description="importance of these changes")
    value: int = Field(description='value of these changes', ge=0, le=10)


dev_support_agent = Agent(  

    'gemini-1.5-flash',  

    deps_type=SupportDependencies,
    result_type=SupportResult,


    system_prompt=(  
        'You are a developer support staff'
        'With these git changes for each commit'
        'create a progress report with the template structure that outlines these changes,'
        'each change corresponds to the changes in the commit as well as taking into account the commit message'
        "the summary should summarize all the changes, and start with the focus for this week"
        "the progress section should have all the changes in a human readable way, as a list of changes"
        "the importance section should identify why these changes are necessary and evaluation of these changes,"
        "and value fhould range from 1-10 for their effort"
    ),
)

@dev_support_agent.tool
def get_template(
    ctx: RunContext[SupportDependencies]
) -> dict:
    return ctx.deps.template

@dev_support_agent.tool  
async def git_changes(
    ctx: RunContext[SupportDependencies]
) -> str:
    """Returns the changes of the github repo"""  
    return await ctx.deps.changes.get_changes()

@dev_support_agent.tool  
async def git_last_week_changes(
    ctx: RunContext[SupportDependencies]
) -> str:
    """Returns the changes of the github repo"""  
    return await ctx.deps.changes.get_last_weeks_changes()

