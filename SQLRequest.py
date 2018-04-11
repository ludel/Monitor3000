import sqlite3


class SQLRequest:

    def __init__(self, app):
        self.app = app
        app.config.from_object("secret_config")

    def exe_sql(self, query, commit=False):
        req = sqlite3.connect(self.app.config['BDD']).execute(query)
        if commit:
            req.execute("COMMIT ")
        return req

    def update_site(self, url, id_site):
        query = "UPDATE site SET url = '{}'" \
                " WHERE id = '{}'".format(url, id_site)
        self.exe_sql(query, True)

    def delete_site(self, id_site):
        query = "DELETE FROM 'site' WHERE id = {}".format(id_site)
        self.exe_sql(query, True)

    def new_site(self, url):
        query = "INSERT INTO site (url) VALUES ('{}')".format(url)
        self.exe_sql(query, True)

    def new_response(self, number, site_id):
        query = "INSERT INTO requests (number, siteId) VALUES ({}, {})".format(number, site_id)
        self.exe_sql(query, True)

    def get_all_data_site(self):
        sites = self.exe_sql("SELECT * FROM site")
        return sites.fetchall()

    def get_sites_group_by_id(self):
        query = "SELECT s.id, s.url, r.number FROM site s" \
                " JOIN requests r ON s.id = r.siteId" \
                " GROUP BY r.siteId"
        sites = self.exe_sql(query)
        return sites.fetchall()

    def get_request_where_id(self, id_site):
        query = "SELECT s.url, r.number, r.date FROM site s" \
                " JOIN requests r ON s.id = r.siteId" \
                " WHERE r.siteId = {}".format(id_site)
        sites = self.exe_sql(query)
        return sites.fetchall()

    def get_user_password(self, username):
        query = "SELECT password FROM user " \
                "WHERE pseudo like '{}'".format(username)
        password = self.exe_sql(query)
        return password.fetchone()[0]

    def get_url_where(self, id_site):
        query = "SELECT url FROM site" \
                " WHERE id == {}".format(id_site)
        url = self.exe_sql(query)
        return url.fetchone()
