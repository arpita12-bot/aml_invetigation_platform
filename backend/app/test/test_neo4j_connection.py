from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "Neo4j@123"   # same as .env

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD),
)

try:
    driver.verify_connectivity()
    print("Connected successfully!")

    with driver.session() as session:
        result = session.run("RETURN 1 AS value")
        print(result.single()["value"])

except Exception as e:
    print(type(e).__name__)
    print(e)

finally:
    driver.close()