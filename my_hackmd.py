"""
Usage:

api = API(your_access_token)

user_notes = api.get_note_list()
new_note_data = api.create_note(
    title="My Ha",
    content="# Ha\nhahaha",
    permalink='userhahaha')

team_notes = api.get_team_note_list('team-path')
new_note_data = api.create_team_note(
    'team-path',
    title="The Big Ha",
    content="# Ha\nhahaha",
    permalink='teamhahaha')
"""

import json
import requests

class API():
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}

    def get_me(self):
        url = "https://api.hackmd.io/v1/me"
        res = self.request("GET", url)
        return json.loads(res.text)

    def get_teams(self):
        url = "https://api.hackmd.io/v1/teams"
        res = self.request("GET", url)
        return json.loads(res.text)

    def get_team_note_list(self, team):
        url = f"https://api.hackmd.io/v1/teams/{team}/notes"
        res = self.request("GET", url)
        return json.loads(res.text)
        
    def get_note_list(self):
        url = "https://api.hackmd.io/v1/notes"
        res = self.request("GET", url)
        return json.loads(res.text)

    def get_team_note(self, team, note_id):
        assert len(note_id) == 22, "note_id should have length 22."
        url = f"https://api.hackmd.io/v1/teams/{team}/notes/{note_id}"
        res = self.request("GET", url)
        return json.loads(res.text)

    def get_note(self, note_id):
        assert len(note_id) == 22, "note_id should have length 22."
        url = f"https://api.hackmd.io/v1/notes/{note_id}"
        res = self.request("GET", url)
        return json.loads(res.text)

    def create_note(
        self,
        title="",
        content="",
        read_permission="guest",
        write_permission="owner",
        comment_permission="everyone",
        permalink=None,
        url="https://api.hackmd.io/v1/notes"):
        """
        permissions: "owner", "signed_in", "guest"
        """
        post_data = {
            "title": title,
            "content": content,
            "readPermission": read_permission,
            "writePermission": write_permission,
            "commentPermission": comment_permission
        }
        if permalink:
            post_data['permalink'] = permalink
        res = self.request(
            "POST",
            url,
            data=post_data)
        return json.loads(res.text)

    def create_team_note(
        self, team,
        title="",
        content="",
        read_permission="guest",
        write_permission="signed_in",
        comment_permission="everyone",
        permalink=None,
        ):
        return self.create_note(
            title=title,
            content=content,
            read_permission=read_permission,
            write_permission=write_permission,
            comment_permission=comment_permission,
            permalink=permalink,
            url=f"https://api.hackmd.io/v1/teams/{team}/notes")

    def update_note(
        self, note_id,
        title=None,
        content=None,
        read_permission=None,
        write_permission=None,
        comment_permission=None,
        permalink=None,
        url="https://api.hackmd.io/v1/notes/"
        ):
        assert len(note_id) == 22, "note_id should have length 22."
        url_plus_id = url + note_id
        post_data = {}
        for key, value in (
            ("title", title),
            ("content", content),
            ("readPermission", read_permission),
            ("writePermission", write_permission),
            ("commentPermission", comment_permission),
            ("permalink", permalink),
            ):
            if value:
                post_data[key] = value
        res = self.request(
            "PATCH",
            url_plus_id,
            data=post_data)
        return res.text

    def update_team_note(
        self, team, note_id,
        title=None,
        content=None,
        read_permission=None,
        write_permission=None,
        comment_permission=None,
        permalink=None,
        ):
        return self.update_note(
            note_id,
            title=title,
            content=content,
            read_permission=read_permission,
            write_permission=write_permission,
            comment_permission=comment_permission,
            permalink=permalink,
            url=f"https://api.hackmd.io/v1/teams/{team}/notes/")

    def delete_note(self, note_id):
        url = f"https://api.hackmd.io/v1/notes/{note_id}"
        res = self.request("DELETE", url)
        return res.text

    def delete_team_note(self, team, note_id):
        url = f"https://api.hackmd.io/v1/teams/{team}/notes/{note_id}"
        res = self.request("DELETE", url)
        return res.text

    def get_note_read_history(self):
        url = "https://api.hackmd.io/v1/history"
        res = self.request("GET", url)
        return json.loads(res.text)

    def request(self, method, url, data=None):
        """
        A wrapper to requests
        """
        methods = {
            "GET": requests.get,
            "POST": requests.post,
            "PATCH": requests.patch, 
            "DELETE": requests.delete,}
        try:
            if data:
                result = methods[method](url, json=data, headers=self.headers)
            else:
                result = methods[method](url, headers=self.headers)
            result.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print ("Error:", err)
        return result
