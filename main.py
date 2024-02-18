import os
import sqlalchemy


from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from db.models import create_tables
from parsing import parsing_pdf


if __name__ == "__main__":  

    load_dotenv()
    DSN = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    parsing_pdf("SAE J1939-71.pdf", session)

    session.close()
    