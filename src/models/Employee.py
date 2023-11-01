from neo4j import GraphDatabase, Driver
from src.models.Driver import _get_connection

class Employee:
    def __init__(self, name, address, branch):
        """Initialize an Employee object with the provided attributes."""

        self.name = name
        self.address = address
        self.branch = branch

def list_of_employees():
    """Retrieve a list of all employees from the database."""

    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (e:Employee) RETURN ID(e) as id, e.name as name, e.address as address, e.branch as branch"
                )
                employees = [{
                        'id': record["id"],
                        'name': record["name"],
                        'address': record["address"],
                        'branch': record["branch"]
                    }
                    for record in result]
                return employees
            except Exception as e:
                print(f"Error: {e}")
                return []

    else:
        print("The driver is not connected")
        return []

def is_valid_employee(id):
    """Checks if the given employee ID is valid."""

    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (e:Employee) WHERE ID(e) = $id RETURN e",
                    id=id
                )
                return bool(result.single())  # Check if a result exists
            except Exception as e:
                print(f"Error: {e}")
                return False  # Return False on error
    return False  # Return False if the driver is not connected

def add_employee(name, address, branch):
    """Add a new employee to the database with the provided details."""

    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                session.run(
                    "CREATE (e:Employee {name: $name, address: $address, branch: $branch})",
                    name=name,
                    address=address,
                    branch=branch
                )
                print(f"Employee added: Name - {name}, Branch - {branch}")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")

def update_employee(id, newName=None, newAddress=None, newBranch=None):
    """Update the details of an employee with the given ID."""

    if not is_valid_employee(id):
        raise Exception(f"No employee found with ID: {id}")
    
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                query = "MATCH (e:Employee) WHERE ID(e) = $id "
                if newName:
                    query += "SET e.name = $newName "
                if newAddress:
                    query += "SET e.address = $newAddress "
                if newBranch:
                    query += "SET e.branch = $newBranch "
                session.run(query, id=id, newName=newName, newAddress=newAddress, newBranch=newBranch)
                print(f"Employee with ID {id} updated successfully!")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")

def delete_employee(id):
    """Delete an employee with the given ID from the database."""
    
    if not is_valid_employee(id):
        raise Exception(f"No employee found with ID: {id}")
    
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                session.run(
                    "MATCH (e:Employee) WHERE ID(e) = $id DELETE e",
                    id=id
                )
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")
