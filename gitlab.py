from base64 import b64encode
from http.client import HTTPConnection, HTTPSConnection
import json
from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen
from issuetracker import IssueTracker, Issue, Comment

class GitlabIssues(IssueTracker):

    def __init__(self):
        self.host = None
        self.headers = {
            "User-Agent": self.user_agent,
            "PRIVATE-TOKEN": self.get_auth_header()
        }

    def new_connection(self):
        if not self.host:
            self.host = input("Gitlab host: ")
        if self.host.endswith("+"):
            return HTTPSConnection(self.host[:-1])
        else:
            return HTTPConnection(self.host)

    def get_auth_header(self):
        return input("Gitlab private token: ")

    def get_project_id(self, project):
        client = self.new_connection()
        client.request("GET", "/api/v3/projects/%s" % (quote_plus(project)), headers=self.headers)

        resp = client.getresponse()
        if not resp.status == 200:
            print("error getting the project id")
            return -1

        return json.loads(resp.read().decode())["id"]

    def get_issues(self, project):

        project_id = self.get_project_id(project)

        client = self.new_connection()
        client.request("GET", "/api/v3/projects/%d/issues" % project_id, headers=self.headers)

        resp = client.getresponse()

        if not resp.status == 200:
            print("error getting issues", resp.status)
            return []

        content = json.loads(resp.read().decode())

        issues = []
        for issue in content:

            obj = Issue(
                issue["iid"],
                issue["author"]["username"],
                issue["assignee"]["username"] if issue["assignee"] else None,
                False if issue["state"] == "closed" else True,
                issue["title"],
                issue["description"],
                []
            )

            issues.append(obj)

        return issues

    def import_issue(self, project, issue):

        project_id = self.get_project_id(project)

        # TODO sudo to keep name

        return super().import_issue(issue)
