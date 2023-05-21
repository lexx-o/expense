import sqlalchemy
from sqlalchemy import create_engine


def create_pg_engine(host: str, port: str, db: str, user: str, passwd: str) -> sqlalchemy.Engine:
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    engine = create_engine(url)
    return engine


pg_engine = create_pg_engine(
                    host="postgres-db",
                    port="5432",
                    db="postgres",
                    user="postgres",
                    passwd="pg_pass")