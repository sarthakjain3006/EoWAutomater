import asyncio
from git import Repo, InvalidGitRepositoryError
import os
from datetime import datetime, timedelta, timezone
GITHUB_REPO_NAME = "EoWAutomater"
class GitChanges():
    def __init__(self):
        self.repo_path = f'./repo-collection/{GITHUB_REPO_NAME}/'
        self.repo_url = f'https://github.com/sarthakjain3006/{GITHUB_REPO_NAME}.git'

    async def get_changes(self):
        res = ""

        # Initialize or fetch the repository
        repo, status = self._initialize_or_fetch_repo()
        res += status
        if not repo:
            return res

        # Iterate through branches
        for branch_name in self._get_branch_names(repo):
            res += f"Checking branch: {branch_name}\n"

            # Checkout the branch
            repo.git.checkout(branch_name)

            # Pull latest changes
            res += f"Pulling latest changes for branch: {branch_name}\n"
            repo.git.pull()

            # Process commits and diffs
            res += f"Processing commits for branch: {branch_name}\n"
            res += self._process_commits(repo, branch_name)

        return res

    async def get_last_weeks_changes(self):
        res = ""

        # Initialize or fetch the repository
        repo, status = self._initialize_or_fetch_repo()
        res += status
        if not repo:
            return res

        # Filter commits from the last 7 days
        est_timezone = timezone(timedelta(hours=-5))  # EST is UTC-5

        # Calculate one week ago in EST
        one_week_ago = datetime.now(tz=est_timezone) - timedelta(days=7)

        for branch_name in self._get_branch_names(repo):
            res += f"Checking branch: {branch_name}\n"

            # Checkout the branch
            repo.git.checkout(branch_name)

            # Pull latest changes
            res += f"Pulling latest changes for branch: {branch_name}\n"
            repo.git.pull()

            # Process commits from the last week
            res += f"Processing commits for branch: {branch_name} (last 7 days)\n"
            res += self._process_commits(repo, branch_name, since=one_week_ago)

        return res

    def _initialize_or_fetch_repo(self):
        if os.path.exists(self.repo_path):
            try:
                repo = Repo(self.repo_path)
                if repo.remotes.origin.url != self.repo_url:
                    return None, "Existing repository does not match the URL. Please resolve this.\n"
                repo.git.fetch('--all')
                return repo, "Repository already exists. Fetching latest changes...\n"
            except InvalidGitRepositoryError:
                return None, "Directory exists but is not a valid Git repository.\n"
        else:
            repo = Repo.clone_from(self.repo_url, self.repo_path)
            return repo, "Cloning repository...\n"

    def _get_branch_names(self, repo):
        return [ref.name.split('/')[-1] for ref in repo.remotes.origin.refs]

    def _process_commits(self, repo, branch_name, since=None):
        res = ""
        for commit in repo.iter_commits(branch_name):
            commit_time = commit.committed_datetime
            if since and commit_time < since:
                continue

            res += f"Commit Hash: {commit.hexsha}\n"
            res += f"Author: {commit.author.name} <{commit.author.email}>\n"
            res += f"Date: {commit.committed_datetime}\n"
            res += f"Message: {commit.message}\n"
            res += "-" * 50 + "\n"

            # Generate diffs for the commit
            if commit.parents:
                parent = commit.parents[0]
                diffs = parent.diff(commit, create_patch=True)
                for diff in diffs:
                    res += f"File: {diff.a_path or diff.b_path}\n"
                    res += diff.diff.decode('utf-8') + "\n"
                    res += "=" * 50 + "\n"
            else:
                res += "Initial commit. No diffs available.\n"
                res += "=" * 50 + "\n"
        print(res)
        return res
    
if __name__ == "__main__":
    asyncio.run(GitChanges().get_last_weeks_changes())
