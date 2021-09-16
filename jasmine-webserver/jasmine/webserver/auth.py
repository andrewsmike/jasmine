"""
WIP
"""
from functools import cache
from typing import Any

from ariadne.types import GraphQLResolveInfo
from requests_oauthlib import OAuth2Session

from jasmine.webserver.app_base import app_config


@cache
def github_oauth_creds():
    return dict(app_config()["github_oauth"])


# auth.oauth_login()
def resolve_oauth_login(obj: Any, info: GraphQLResolveInfo):
    creds = github_oauth_creds()

    oauth2_handle = OAuth2Session(creds["client_id"])
    authorization_url, state = oauth2_handle.authorization_url(
        creds["authorization_base_url"],
    )
    info.context["github_oauth_login_state"] = state

    return authorization_url


# auth.oauth_login_callback()
def resolve_oauth_login_callback(obj: Any, info: GraphQLResolveInfo, auth_response_url):
    creds = github_oauth_creds()
    oauth2_handle = OAuth2Session(
        creds["client_id"], state=info.context["github_oauth_login_state"]
    )
    info.context["github_oauth_token"] = oauth2_handle.fetch_token(
        creds["token_url"],
        client_secret=creds["client_secret"],
        authorization_response=auth_response_url,
    )

    return oauth2_handle.get("https://api.github.com/user").json()
