import asyncio
from dev_support import SupportDependencies, dev_support_agent
from changes.changes import GitChanges

async def main():
    deps = SupportDependencies(changes=GitChanges())
    result = await dev_support_agent.run('What is my report?', deps=deps)  
    print(result.data)  


if __name__ == "__main__":
    asyncio.run(main())
