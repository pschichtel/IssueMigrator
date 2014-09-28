from github import GithubIssues
from gitlab import GitlabIssues

gitlab = GitlabIssues()
github = GithubIssues()

issues = gitlab.get_issues("example/Example")

for issue in issues:
    github.import_issue("example/Example", issue)
