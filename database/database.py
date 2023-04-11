from pymongo import MongoClient

import os
from dotenv import load_dotenv
#  load environment variables from .env file
load_dotenv()

# # # get environment variables
# # # MONGODB_URI = os.getenv('MONGODB_URI')
# # # print(MONGODB_URI)
MONGODB_URI= os.environ.get('MONGODB_URL')
print(MONGODB_URI)
DB_NAME = os.environ.get('DATABASE_NAME')
# COLLECTION_NAME = os.environ.get('COLLECTION_NAME')


client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
eventCollection = db.events



    


