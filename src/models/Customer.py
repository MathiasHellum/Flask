from neo4j import GraphDatabase, Driver
from src.models.Driver import _get_connection
import re

class Customer:
    def __init__(self, name, email, phone_number):
        """Initialize a Customer object with the provided attributes."""
        self.name = name
        self.email = email
        self.phone_number = phone_number


def list_of_customers():
    """Retrieve a list of all customers from the database."""
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (c:Customer) RETURN ID(c) as id, c.name as name, c.email as email, c.phone_number as phone_number"
                )
                customers = [{
                        'id': record["id"],
                        'name': record["name"],
                        'email': record["email"],
                        'phone_number': record["phone_number"]
                    }
                    for record in result]
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")
    return customers


def is_valid_customer(customer_id):
    """Checks if the given customer ID is valid"""

    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (c:Customer) WHERE ID(c) = $customer_id RETURN c",
                    customer_id=customer_id
                )
                return bool(result.single())  # Check if a result exists
            except Exception as e:
                print(f"Error: {e}")
                return False  # Return False on error
    return False  # Return False if the driver is not connected


def add_customer(name, email, phone_number):
    """Add a new customer to the database with the provided details."""
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                session.run(
                    "CREATE (c:Customer {name: $name, email: $email, phone_number: $phone_number})",
                    name=name,
                    email=email,
                    phone_number=phone_number
                )
                print(f"Customer added: Name - {name}, Email - {email}")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")


def update_customer(id, name=None, email=None, phone_number=None):
    """Update the details of a customer with the given ID."""

    if not is_valid_customer(id):
        raise Exception(f"No customer found with ID: {id}")
    
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                # Build the update query dynamically based on the fields provided
                updates = []
                params = {'id': id}
                if name:
                    updates.append("c.name = $name")
                    params['name'] = name
                if email:
                    updates.append("c.email = $email")
                    params['email'] = email
                if phone_number:
                    updates.append("c.phone_number = $phone_number")
                    params['phone_number'] = phone_number
                
                update_string = ", ".join(updates)
                query = f"MATCH (c:Customer) WHERE ID(c) = $id SET {update_string}"
                
                session.run(query, **params)
                print(f"Customer with ID {id} updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")


def delete_customer(id):
    """Delete a customer with the given ID from the database."""

    if not is_valid_customer(id):
        raise Exception(f"No customer found with ID: {id}")

    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                session.run(
                    "MATCH (c:Customer) WHERE ID(c) = $id DELETE c",
                    id=id
                )
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")
