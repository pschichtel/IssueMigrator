from getpass import getpass


class IssueTracker:

    user_agent = "Cube Island Issue Transformer"

    def get_issues(self, project):
        raise NotImplementedError("get_issues not implemented!")

    def import_issue(self, project, issue):
        raise NotImplementedError("import_issue not implemented")


class Issue:

    def __init__(self, id, author, assignee, state, title, content, comments):
        self.id = id
        self.author = author
        self.assignee = assignee
        self.state = state
        self.title = title
        self.content = content
        self.comments = comments

    def __str__(self):
        return "#%s" % self.id


class Comment:

    def __init__(self, author, content):
        self.author = author
        self.content = content
