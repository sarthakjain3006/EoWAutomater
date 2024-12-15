
from template import WeeklyUpdate
from changes.gitchanges import GitChanges
from langchain_google_genai import ChatGoogleGenerativeAI


def main():
    git_changes_instance = GitChanges()
    changes = git_changes_instance.get_last_weeks_changes()
    template = WeeklyUpdate()
    # Pass the GitChanges instance to SupportDependencies
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
    
    structured_llm = llm
    result = structured_llm.invoke(
        'You are a developer support staff' + "\n" + 
        'With these git changes for each commit' + "\n" + 
        changes + "\n" + 
        'complete a progress report with the following template structure that outlines these changes,' + "\n" + 
        template.model_dump_json() + "\n" + 
        'each change is a string corresponds to the changes in the commit as well as taking into account the commit message, with more weight on summarizing the changes themselves over the commit message'+ "\n" +
        "the changes should also contain a summarizing impact string at the very end, which should explain why these changes are necessary" 
        "the summary should summarize all the changes, in a brief and concise manner,  and start with the focus for this week which should summarize the biggest feature changes in the code. Only mention important high level changes and exclude any minor changes here" + "\n" +
        "the progress section should have all the changes in a human readable way, in a dictionary where the key string item is a feature headline and the value a list of changes for those items" + "\n" +
        "the roadblocks section should only be used if there are any visible roadblocks in the commit messages or the changes are not functional" + "\n" +
        "keep the length concise for each progress and roadblock, making them a culmination of changes and roadblock items from multiple commits and prioritise making multiple concise changes over a large block of string " + "\n" +
        "the next weeks work should gather all the changes and create a list of all possible optimizations, security, maintenance or deployment changes, prioritizing those mentioned in the commit messages or TODO comments in the code changes" + "\n" +
        ""
    )
    print(result.content  )


if __name__ == "__main__":
    main()
