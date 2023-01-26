import enum
import os

from sqlalchemy import Column, DateTime, Enum, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import URLType

db_string = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432")
echo = os.getenv("SQL_ECHO", "0")

db = create_engine(db_string, echo=(echo == "1"), isolation_level="READ COMITTED")

Session = sessionmaker(db)
base = declarative_base()


class Network(enum.Enum):
    twitter = 0
    vkontakte = 1


class Post(base):
    __tablename__ = "posts"
    url = Column(URLType, primary_key=True)
    text = Column(Text)
    publication_date = Column(DateTime, index=True)
    network = Column(
        Enum(Network), index=True
    )  # Index might not be useful as it returns more than 10% of the lines and postgres will prefer a SEQSCAN.


base.metadata.create_all(db)


def bulk_posts_insert(posts):
    """
    Method to make bulk insert into the DB which is quicker than inserting every new Post one by one.
    """
    with Session.begin() as session:
        session.add_all(posts)
