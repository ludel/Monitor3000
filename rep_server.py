from requests import request


def get_response(sites):
    dict_response = {}
    for site in sites:
        dict_response[site[0]] = request('get', site[1]).status_code
    return dict_response
