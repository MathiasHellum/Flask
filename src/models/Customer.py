from neo4j import GraphDatabase, Driver
from src.models.Driver import _get_connection
import re
from src.models.Car import get_car_by_id, update_car

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


def has_customer_booked_or_rented(customer_id):
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (cust:Customer)-[:BOOKED|Rented]->(car:Car) WHERE ID(cust) = $customer_id RETURN car",
                    customer_id=customer_id
                )
                record = result.single()
                return True if record else False
            except Exception as e:
                print(e)
    return False


def link_customer_to_car(customer_id, car_id, relationship_type):
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                relationship_query = (
                    f"MATCH (cust:Customer), (car:Car) "
                    f"WHERE ID(cust) = $customer_id AND ID(car) = $car_id "
                    f"CREATE (cust)-[:{relationship_type}]->(car)"
                )
                session.run(relationship_query, customer_id=customer_id, car_id=car_id)
                return True
            except Exception as e:
                print(e)
    return False



def book_car_for_customer(car_id, customer_id):
    # First, check if the car is available and the customer hasn't already booked/rented a car.
    car_details = get_car_by_id(car_id)
    customer_status = has_customer_booked_or_rented(customer_id)

    if not car_details:
        raise ValueError("The specified car does not exist.")
    if car_details['status'] != 'available':
        raise ValueError("The specified car is not available for booking.")
    if customer_status:
        raise ValueError("The customer has already booked or rented a car.")

    # If all checks pass, link the customer to the car with a BOOKED relationship and update the car status.
    link_status = link_customer_to_car(customer_id, car_id, "BOOKED")
    try:
        update_car(car_id, "booked")
        car_update_status = True
    except Exception as e:
        print(e)
        car_update_status = False

    if link_status and car_update_status:
        return True
    else:
        raise Exception("Failed to book the car for the customer.")


def find_customer_by_name_and_phone(name, phone_number):
    """Finds a customer based on their name and phone number."""
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (c:Customer) WHERE c.name = $name AND c.phone_number = $phone_number RETURN ID(c) as id, c.name as name, c.email as email, c.phone_number as phone_number",
                    name=name,
                    phone_number=phone_number
                )
                record = result.single()
                if record:
                    return {
                        'id': record["id"],
                        'name': record["name"],
                        'email': record["email"],
                        'phone_number': record["phone_number"]
                    }
            except Exception as e:
                print(f"Error: {e}")
    return None
