from git import Repo, InvalidGitRepositoryError
import os
from constants import GITHUB_REPO_NAME

class GitChanges:
    async def get_changes(self):
        repo_path = f'./repo-collection/{GITHUB_REPO_NAME}/'
        repo_url = f'https://github.com/sarthakjain3006/{GITHUB_REPO_NAME}.git'
        res = ""

        # Check if the repository exists
        if os.path.exists(repo_path):
            try:
                repo = Repo(repo_path)
                if repo.remotes.origin.url != repo_url:
                    res += "\nExisting repository does not match the URL. Please resolve this."
                    return res
                res += "Repository already exists. Pulling latest changes...\n"
                repo.git.fetch('--all')  # Fetch all updates from remote
            except InvalidGitRepositoryError:
                res += "Directory exists but is not a valid Git repository.\n"
                return res
        else:
            res += "Cloning repository...\n"
            repo = Repo.clone_from(repo_url, repo_path)

        # Iterate through branches
        for remote_ref in repo.remotes.origin.refs:
            branch_name = remote_ref.name.split('/')[-1]
            res += f"Checking branch: {branch_name}\n"

            # Checkout the branch
            repo.git.checkout(branch_name)

            # Pull latest changes
            res += f"Pulling latest changes for branch: {branch_name}\n"
            repo.git.pull()

            # Check for commits and show diffs
            res += f"Processing commits for branch: {branch_name}\n"
            for commit in repo.iter_commits(branch_name):
                res += f"Commit Hash: {commit.hexsha}\n"
                res += f"Author: {commit.author.name} <{commit.author.email}>\n"
                res += f"Date: {commit.committed_datetime}\n"
                res += f"Message: {commit.message}\n"
                res += "-" * 50 + "\n"

                # Generate and collect the diff for the commit
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

        return res
