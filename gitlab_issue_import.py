__author__ = 'Phillip'

import http.client, urllib.parse

headers = {'PRIVATE-TOKEN': '<private token>'}
project = 13


data = open('data.csv', 'r')

for line in data:
    line = line.strip()
    comma = line.find(',')

    if comma >= 0:
        body = {
            'title': line[:comma].strip(),
            'description': line[comma+1:].strip().replace("\\n", "\n")
        }
    else:
        body = {
            'title': line
        }

    print(body["title"])
    if "description" in body:
        print(body["description"])
    print("\n\n")

    client = http.client.HTTPConnection('git.cubeisland.de')
    client.request('POST', '/api/v3/projects/%d/issues' % project, urllib.parse.urlencode(body), headers)
    resp = client.getresponse()

    if resp.status < 300:
        print("Success!")
    else:
        print("Failure!")

    #print(resp.status, resp.headers, resp.read())
