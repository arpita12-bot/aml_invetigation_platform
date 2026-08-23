from neo4j import GraphDatabase

from app.core.config import settings


class Neo4jConnection:

    _driver = None

    @classmethod
    def driver(cls):

        if cls._driver is None:

            cls._driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(
                    settings.NEO4J_USERNAME,
                    settings.NEO4J_PASSWORD,
                ),
            )

            cls._driver.verify_connectivity()

        return cls._driver
    
    @classmethod
    def session(cls):
        """
        Returns a Neo4j session using the configured database.
        """
        return cls.driver().session(
            database=settings.NEO4J_DATABASE
        )

    @classmethod
    def close(cls):

        if cls._driver:

            cls._driver.close()

            cls._driver = None