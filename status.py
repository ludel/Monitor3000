from requests import request
from app import exec_sql
from time import sleep


def get_response():
    dict_response = {}
    sites = exec_sql("SELECT id, url FROM site ").fetchall()
    for site in sites:
        dict_response[site[0]] = request('get', site[1]).status_code
    return dict_response


def update_status(dict_response):
    for key, value in dict_response.items():
        exec_sql("INSERT INTO requests (number, siteId) VALUES ({}, {})".format(value, key), True)


if __name__ == '__main__':

    while True:
        print("===============================")
        response = get_response()
        update_status(response)
        sleep(120)
