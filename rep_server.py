from requests import request, exceptions


def get_response(sites):
    dict_response = {}
    for site in sites:
        try:
            dict_response[site[0]] = request('get', site[1]).status_code
        except exceptions.MissingSchema:
            dict_response[site[0]] = 400
        except exceptions.InvalidSchema:
            dict_response[site[0]] = 400
        except exceptions.SSLError:
            dict_response[site[0]] = 495
        except exceptions.ConnectionError:
            dict_response[site[0]] = 504
    return dict_response
