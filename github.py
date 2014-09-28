from base64 import b64encode
from http.client import HTTPConnection, HTTPSConnection
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from issuetracker import IssueTracker, Issue, Comment


class GithubIssues(IssueTracker):

    def __init__(self):
        super(IssueTracker, self).__init__()
        self.headers = {
            "User-Agent": self.user_agent,
            "Authorization": self.get_auth_header()
        }

    def new_connection(self):
        return HTTPSConnection("api.github.com")

    def get_auth_header(self):
        return "token %s" % input("Github OAUTH token: ")

    def get_issues(self, project):
        client = self.new_connection()
        client.request('GET', '/repos/%s/issues' % project, headers=self.headers)
        resp = client.getresponse()
        content = resp.read().decode()
        response = json.loads(content)
        resp.close()
        client.close()

        issues = []

        for issue in response:

            comments = []
            for comment in response:
                comments.append(
                    Comment(
                        comment["user"]["login"],
                        comment["body"]
                    )
                )

            obj = Issue(
                issue["number"],
                issue["user"]["login"],
                issue["assignee"]["login"] if issue["assignee"] else None,
                True if issue["state"] == "open" else False,
                issue["title"],
                issue["body"],
                comments
            )
            issues.append(obj)

            client = self.new_connection()
            client.request("GET", issue["comments_url"], headers=self.headers)

            resp = client.getresponse()
            response = json.loads(resp.read().decode())
            resp.close()
            client.close()

        return issues

    def import_issue(self, project, issue):

        client = self.new_connection()
        client.request("GET", "/user", headers=self.headers)
        resp = client.getresponse()
        content = json.loads(resp.read().decode())
        if not resp.status == 200:
            print("error getting the current user")
            return

        currentUser = content["login"]

        data = {
            "title": issue.title,
            "body": issue.content,
            "assignee": issue.assignee
        }

        client = self.new_connection()
        client.request("POST", "/repos/%s/issues" % project, json.dumps(data), self.headers)

        resp = client.getresponse()
        response = json.loads(resp.read().decode())
        if resp.status == 201:
            if not issue.state:
                data = {
                    "title": issue.title,
                    "state": "open" if issue.state else "closed"
                }
                client = self.new_connection()
                client.request("PATCH", response["url"], json.dumps(data), self.headers)
                resp = client.getresponse()
                if not resp.status == 200:
                    print("error while editing")
                    pass  # TODO error handling

            for comment in issue.comments:
                client = self.new_connection()
                data = {
                    "body": comment.content
                }
                if comment.author != currentUser:
                    data["body"] = "%s:\n\n%s" % (comment.author, "    " + data["body"].replace("\n", "\n    "))

                client.request("POST", response["comments_url"], json.dumps(data), self.headers)

                resp = client.getresponse()
                if not resp.status == 201:
                    print("Error creating comment!")

        else:
            print("error creating issue", response)
