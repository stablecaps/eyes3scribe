# https://pygithub.readthedocs.io/en/stable/introduction.html
# Authentication is defined via github.Auth
import argparse
import os
import sys

from github import Auth, Github

# a. Only allow squash merging (disable merge & rebase)
# b. Set squash merge to "Pull request title & description"
# c. Automatically delete head branches
# d. Protect master branch:
#     xi. Require pull request reviews before merging
#     xii. Require approvals (1)
#     xiii. Dismiss stale pull request approvals when new commits are pushed
#     xiv. Require review from Code Owners
#     v. Restrict who can dismiss pull request reviews (i.e. DPArts)
#     vi. Allow specified actors to bypass required pull requests (i.e. DPArts)
#     vii. other options unchecked


class ModGithubSettings:
    def __init__(self, token, owner, repository):
        self.token = token
        self.owner = owner
        self.repository = repository

    def main(self):
        ghub = Github(self.token)
        repo = ghub.get_repo(f"{self.owner}/{self.repository}")
        print(f"Repository: {repo.full_name}")
        # print(dir(repo))
        repo.edit(
            allow_merge_commit=False,
            allow_squash_merge=True,
            allow_rebase_merge=False,
            # squash_merge_commit_message="PR_TITLE and PR_BODY", # issue submitted https://github.com/PyGithub/PyGithub/issues/2890
            delete_branch_on_merge=True,
        )

        branch = repo.get_branch("master")
        branch.edit_protection(
            required_approving_review_count=1,
            enforce_admins=False,
            users_bypass_pull_request_allowances=["darkpandarts"],
        )

        branch.edit_required_pull_request_reviews(
            dismissal_users=["darkpandarts"],
            dismissal_teams=["darkpandarts"],
            dismissal_apps=["darkpandarts"],
            dismiss_stale_reviews=True,
            require_code_owner_reviews=True,
            required_approving_review_count=1,
        )

        ghub.close()

        #


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modify GitHub repository settings")
    parser.add_argument(
        "-t", "--token", required=True, help="GitHub personal access token"
    )
    parser.add_argument(
        "-o",
        "--owner",
        required=False,
        default="stablecaps",
        help="GitHub repository owner. e.g. stablecaps",
    )
    parser.add_argument(
        "-r", "--repository", required=True, help="GitHub repository name"
    )

    args = parser.parse_args()

    # using an access token
    auth = Auth.Token(args.token)

    mgs = ModGithubSettings(args.token, args.owner, args.repository)
    mgs.main()
