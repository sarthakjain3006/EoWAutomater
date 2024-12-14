from git import Repo, InvalidGitRepositoryError
import os
from constants import GITHUB_REPO_NAME
class GitChanges():
    async def get_changes(self):
        repo_path = f'./repo-collection/{GITHUB_REPO_NAME}/'
        repo_url = f'https://github.com/sarthakjain3006/{GITHUB_REPO_NAME}.git'

        # Check if the repository exists
        if os.path.exists(repo_path):
            try:
                repo = Repo(repo_path)
                if repo.remotes.origin.url != repo_url:
                    print("Existing repository does not match the URL. Please resolve this.")
                    return
                print("Repository already exists. Pulling latest changes...")
                repo.git.fetch('--all')  # Fetch all updates from remote
            except InvalidGitRepositoryError:
                print("Directory exists but is not a valid Git repository.")
                return
        else:
            print("Cloning repository...")
            repo = Repo.clone_from(repo_url, repo_path)

        # Iterate through branches
        for remote_ref in repo.remotes.origin.refs:
            branch_name = remote_ref.name.split('/')[-1]
            print(f"Checking branch: {branch_name}")

            # Checkout the branch
            repo.git.checkout(branch_name)

            # Pull latest changes
            print(f"Pulling latest changes for branch: {branch_name}")
            repo.git.pull()

            # Check for commits and show diffs
            print(f"Processing commits for branch: {branch_name}")
            for commit in repo.iter_commits(branch_name):
                print(f"Commit Hash: {commit.hexsha}")
                print(f"Author: {commit.author.name} <{commit.author.email}>")
                print(f"Date: {commit.committed_datetime}")
                print(f"Message: {commit.message}")
                print("-" * 50)

                # Generate and print the diff for the commit
                if commit.parents:
                    parent = commit.parents[0]
                    diffs = parent.diff(commit, create_patch=True)
                    for diff in diffs:
                        print(f"File: {diff.a_path or diff.b_path}")
                        print(diff.diff.decode('utf-8'))
                        print("=" * 50)
                else:
                    print("Initial commit. No diffs available.")
                    print("=" * 50)