from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re

URI = "neo4j+s://992844cb.databases.neo4j.io"
AUTH = ("neo4j", "agX8W2AHT6s5D0vjnJwdU1nFe3redVb7FAHtWvP3d9M")


def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    return driver

def findUserByUsername(username):
    data = _get_connection().execute_query("MATCH (a:User) where a.username = $username RETURN a;", username=username)
    if len(data[0]) > 0:
        user = User(username, data[0][0][0]['email'])
        return user
    else:
        return User(username, "Not found in DB")

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_Username(self):
        return self.username

    def set_Username(self, value):
        self.username = value

    def get_Email(self):
        return self.email

    def set_Email(self, value):
        self.email = value