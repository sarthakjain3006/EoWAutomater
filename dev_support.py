from pydantic_ai import Agent
from dataclasses import dataclass
from changes.changes import GitChanges
from pydantic import BaseModel, Field
from pydantic_ai import RunContext
from template import  raw_template

@dataclass
class SupportDependencies:  
    changes: GitChanges
    template: str = raw_template

class SupportResult(BaseModel):  

    report: str = Field(description="report")
    key_changes: str = Field(description='Changes made')
    importance: bool = Field(description="importance of these changes")
    value: int = Field(description='value of these changes', ge=0, le=10)


dev_support_agent = Agent(  

    'gemini-1.5-flash',  

    deps_type=SupportDependencies,
    result_type=SupportResult,


    system_prompt=(  
        'You are a developer support staff'
        'With these git changes for each commit, create a progress report with the template that outlines these changes,'
        'their importance, and a value from 1-10 for their effort'
    ),
)

@dev_support_agent.tool
def get_template(
    ctx: RunContext[SupportDependencies]
) -> str:
    return ctx.deps.template

@dev_support_agent.tool  
async def git_changes(
    ctx: RunContext[SupportDependencies]
) -> str:
    """Returns the changes of the github repo"""  
    return await ctx.deps.changes.get_changes()

