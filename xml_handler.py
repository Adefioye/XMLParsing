from xml.sax.handler import ContentHandler

import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from .env file
load_dotenv()

class XMLHandler(ContentHandler):

    def __init__(self):
        self.data = {}
        self.table_name = ""
        self.table_names = set(["Event", "Link", "Node"])

    def startElement(self, name, attrs):
        # Get name, Make sure it is capitalized
        # Get attr keys and insert attr values into them

        if name.strip().capitalize() in self.table_names:
            # Collect attributes into a dictionary
            self.data = dict(attrs)

            # Check if name is either node/event replace id with (node|event)_id
            # and then delete origina id property from xml file
            if name.strip().lower() in set(["link", "node"]):
                self.data[f"{name}_id"] = self.data["id"]
                del self.data["id"]

            # Change from -> from_node, to -> to_node, length -> link_length
            if name.strip().lower() == "link":
                self.data["from_node"] = self.data["from"]
                self.data["to_node"] = self.data["to"]
                self.data["link_length"] = self.data["length"]

                # Delete from, to and length attributes
                del self.data["from"]
                del self.data["to"]
                del self.data["length"]

            # Set table name
            self.table_name = name.capitalize()


        # This writes event attributes into a eventAttributes file
        # with the aim of getting unique set of event attributes
        # TODO: You can uncomment if you want to get unique event attributes saved in a file
        # with open("eventAttributes.txt", "a") as f:
        #     f.write(" ".join(attrs.keys()) + "\n")

    def endElement(self, name):
        # Specify the XML element name where you want to insert data
        if name.capitalize() in self.table_names: 
            # Insert data into PostgreSQL
            self.insert_data_into_postgres()

    def characters(self, content):
        pass

    def insert_data_into_postgres(self):
        # Replace these variables with your actual database credentials
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

        # Connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        print("Connected to postgres database...")

        # Create a cursor object
        cursor = conn.cursor()

        # Construct and execute the INSERT statement
        columns = ', '.join(self.data.keys())
        values = ', '.join(['%s'] * len(self.data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"

        cursor.execute(query, list(self.data.values()))
        print(f"Finished inserting a row into {self.table_name} in postgres db...")

        # Commit the transaction and close the cursor and connection
        conn.commit()
        cursor.close()
        conn.close()