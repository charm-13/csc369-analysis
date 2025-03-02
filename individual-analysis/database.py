import os
import dotenv
from sqlalchemy import create_engine

def database_connection():
    dotenv.load_dotenv()
    
    return create_engine(os.environ.get("POSTGRES_URI"))
    
engine = database_connection()