from dotenv import load_dotenv, find_dotenv
from os import getenv

_: bool = load_dotenv(find_dotenv())

conn_string = getenv("DATABASE_URL")

connection_string = str(conn_string).replace(
    "postgresql", "postgresql+psycopg"
)





