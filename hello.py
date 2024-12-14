import asyncio
from dev_support import SupportDependencies, dev_support_agent
from changes.gitchanges import GitChanges

async def main():
    git_changes_instance = GitChanges()
    await git_changes_instance.get_changes()

    # Pass the GitChanges instance to SupportDependencies
    deps = SupportDependencies(changes=git_changes_instance)
    result = await dev_support_agent.run('What is my report for last week?', deps=deps)  
    print(result.data)  


if __name__ == "__main__":
    asyncio.run(main())
