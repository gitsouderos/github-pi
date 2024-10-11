from project.config.settings import GITHUB_ACCESS_TOKEN
from github import Github
from github import Auth

_auth = Auth.Token(GITHUB_ACCESS_TOKEN)
github_client = Github(auth=_auth)
