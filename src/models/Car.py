from neo4j import GraphDatabase, Driver
from src.models.Driver import _get_connection
import re

class Car:
    def __init__(self, make, model, year, location, status):
        self.make = make
        self.model = model
        self.year = year
        self.location = location
        self.status = status

def listCars():
    cars = []
    driver = _get_connection()
    if driver != None:
        with driver.session() as session:
            try:
                result = session.run("MATCH (c:Car) RETURN ID(c) as id, c.make as make, c.model as model, c.year as year, c.location as location, c.status as status")
                for record in result:
                    cars.append({
                    'id' : record["id"],
                    'make' : record["make"],
                    'model' : record["model"],
                    'year' : record["year"],
                    'location' : record["location"],
                    'status' : record["status"]
                    })
                print(cars)
                return cars
            except Exception as e:
                print(f"Error: ",e)
                return cars
    print("Driver not connected")
    return cars

def addCar(make,model,year,location,status):
    driver = _get_connection()
    if driver != None:
        with driver.session() as session:
            try:
                session.run(
                    "CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: $status})",
                    make=make,
                    model=model,
                    year=year,
                    location=location,
                    status=status
                    )
                return
            except Exception as e:
                print(f"Error: {e}")
                return
    print("Driver not connected")
    return

def updateCar(id, newStatus):
    driver = _get_connection()
    if driver != None:
        with driver.session() as session:
            try:
                session.run(
                    "MATCH (c:Car) WHERE ID(c) = $id SET c.status = $newStatus", 
                    id=id, 
                    newStatus=newStatus
                )
                print(f"ID: {id}, New Status: {newStatus}")
                return
            except Exception as e:
                print(f"Error: ",e)
                print(f"{id} is not a Car.")
                return
    print("Driver is not connected")
    return

def deleteCar(id):
    driver = _get_connection()
    if driver != None:
        with driver.session() as session:
            try:
                session.run(
                    "MATCH (c:Car) WHERE ID(c) = $id DELETE c",
                    id=id
                )
                return
            except Exception as e:
                print(f"Error: {e}")
                return
    print("Driver is not connected")
    return