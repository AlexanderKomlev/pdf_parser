import sqlalchemy as sq
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Data(Base):
    __tablename__ = "data"

    primary_id = sq.Column(sq.Integer, primary_key=True)
    id = sq.Column(sq.String(length=10), nullable=False)
    data_length = sq.Column(sq.String(length=10), nullable=False)
    length = sq.Column(sq.String(length=10), nullable=False)
    name = sq.Column(sq.String(length=100), nullable=False)
    rus_name = sq.Column(sq.String(length=100), nullable=False)
    scaling = sq.Column(sq.String(length=50), nullable=False)
    range = sq.Column(sq.String(length=50), nullable=False)
    spn = sq.Column(sq.String(length=10), nullable=False)

    def __str__(self):
        return f"{self.id, self.data_length, self.length, self.name, self.rus_name, self.scaling, self.range, self.spn}"
    

def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    