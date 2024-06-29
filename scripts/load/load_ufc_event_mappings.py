import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Define the database URL
DATABASE_URL = "postgresql://karim:mypassword@localhost:5432/sb_data"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the mapping_betvictor_ufc_event table model
class MappingBetvictorUFCEvent(Base):
    __tablename__ = "mapping_betvictor_ufc_event"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ufc_event_id = Column(Integer)
    ufc_event_name = Column(String(255))
    betvictor_event_name = Column(String(255))


class UFCEventMapping(Base):
    __tablename__ = "ufc_event_mapping"
    external_event_name = Column(String, primary_key=True, nullable=False)
    ufc_event_name = Column(String, nullable=False)
    ufc_event_id = Column(Integer, nullable=False)

# Ensure the table exists
# Base.metadata.create_all(bind=engine)

def load_csv_to_db(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Create a database session
    session = SessionLocal()

    try:
        for _, row in df.iterrows():
            # Create a new record
            record = UFCEventMapping(
                ufc_event_id=row['ufc_event_id'],
                ufc_event_name=row['ufc_event_name'],
                external_event_name=row['betvictor_event_name']
            )
            session.add(record)
        
        # Commit the transaction
        session.commit()
        print(f"Data from {csv_file_path} loaded successfully into mapping_betvictor_ufc_event table.")

    except Exception as e:
        session.rollback()
        print(f"Failed to load data from {csv_file_path}: {str(e)}")

    finally:
        session.close()

def main():
    csv_file_path = './data/betvictor_ufc_events_mapping.csv'
    load_csv_to_db(csv_file_path)

if __name__ == "__main__":
    main()
