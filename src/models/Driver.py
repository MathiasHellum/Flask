from neo4j import GraphDatabase, Driver

# URI = "neo4j+s://992844cb.databases.neo4j.io"
# AUTH = ("neo4j", "agX8W2AHT6s5D0vjnJwdU1nFe3redVb7FAHtWvP3d9M")

URI = "neo4j+s://992844cb.databases.neo4j.io"
AUTH = ("neo4j", "agX8W2AHT6s5D0vjnJwdU1nFe3redVb7FAHtWvP3d9M")

def _get_connection() -> Driver:
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        driver.verify_connectivity()
        return driver
    except Exception as e:
        print(f"Error: ",e)
        return None