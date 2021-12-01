from neo4j import GraphDatabase
from constants import neo4j as neo4jK
from Models.Driver import Driver


if __name__ == "__main__":
    driver = Driver(neo4jK.ADDRESS, neo4jK.USERNAME, neo4jK.PASSWORD)
    res = driver.query('CREATE (Pepe:persona {nombre: "Pepe", edad:21})')
    print(res)