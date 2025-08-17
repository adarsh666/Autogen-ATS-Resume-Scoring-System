 # importing module
from pymongo import MongoClient
import json
from schema.user_details import UserDetails

hostname = "rygleo.h.filess.io"
database = "resume666_peopledesk"
port = "27018"
username = "resume666_peopledesk"
password = "321adbcb33739dda81f9c162921cedd670f8a4e1"

uri = "mongodb://" + username + ":" + password + "@" + hostname + ":" + port + "/" + database

# Connect with the portnumber and host
client = MongoClient(uri)

# Access database
mydatabase = client[database]
collection = mydatabase["resumes"]


def get_collection():
    return collection


def insert_data(resume_data : UserDetails):
    """
    Adds parsed json data to mongodb
    Args:
        resume_data : Resume data generated
    """
    try:
        resume_data = resume_data.model_dump()
        collection.insert_one(resume_data)
        print("DB success")
        return f"Successfully inserted to db" 
    except Exception as e:
        print("DB Fail")
        return f"Error occurred while searching: {str(e)}"