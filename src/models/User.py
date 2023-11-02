from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re
from src.models.Driver import _get_connection


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