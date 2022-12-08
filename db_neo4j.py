import logging

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
import json

class Neo4jApp:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_friendship(self, person1_name, person2_name):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self._create_and_return_friendship, person1_name, person2_name)
            for record in result:
                print("Created friendship between: {p1}, {p2}"
                      .format(p1=record['p1'], p2=record['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": record["p1"]["name"], "p2": record["p2"]["name"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except Neo4jError as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._find_and_return_person, person_name)
            # print(result)
            for record in result:
                print("Found person: {record}".format(record=record))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        query = (
            # "MATCH (Alice:Person) RETURN Alice"
            "MATCH (p:Person)-[r:KNOWS]->(p2:Person) "
            "WHERE p.name = 'Alice' "
            "RETURN p, r, p2"
        )
        result = tx.run(query, person_name=person_name)
        # print(result)
        # records = [record for record in result]
        # print(records)
        for r in result:
            # print(r)
            for tk, tv in r.items():
                # print(tk, tv)
                element_id = tv.element_id
                label = []
                if tk != 'r':
                    label = [l for l in tv.labels]
                else:
                    print(tk, tv)
                propertie = tv['name']
                # print(tk, element_id, label, propertie, type(propertie))

                # print(type(r), r.values())
                # print(json.loads(r))
        print('-' * 30)
        return [record for record in result]

if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    # uri = "neo4j+s://<Bolt url for Neo4j Aura instance>"
    # user = "<Username for Neo4j Aura instance>"
    # password = "<Password for Neo4j Aura instance>"
    user = "neo4j"
    password = "neo4j"
    
    app = Neo4jApp(uri, user, password)
    # app.create_friendship("Alice", "Eric")
    # app.create_friendship("Alice", "Bob")
    # app.create_friendship("Eric", "Chasing")
    # app.create_friendship("Eric", "Kangkang")
    # app.create_friendship("David", "Kangkang")
    app.find_person("Alice")
    app.close()