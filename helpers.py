import os
import json
import requests
import google.oauth2.id_token
import google.auth.transport.requests
import typing

def ping_cloud_function(fn_url:str, params:dict=None, headers:dict=None) -> typing.Any:
    """pings a cloud function

    Args:
        fn_url (str): cloud function url.
        params (dict): dictionary of parameters to pass to function.
        headers (dict): dictionary of headers to pass to function e.g. token.

    Returns: a tuple of (status code, reason) e.g. (200, 'OK')
    """    
    r = requests.post(
    fn_url,
    headers=headers,
    data=params
    )
    #return (r.status_code, r.reason)
    if r.status_code == 200:
        print(f"""Successfully ran cloud function: {fn_url}
        with params: {params}
        headers: Not showing headers!.
        status_code: {r.status_code}.
        reason: {r.reason}.""")
        return r
    else:
        print(r.status_code, r.reason)
        raise ValueError(f"""Error running cloud function: {fn_url}
                         with params: {params}
                         headers: Not showing headers!.
                         status_code: {r.status_code}.
                         reason: {r.reason}.""")

def get_project_id():
    import urllib.request
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    return project_id