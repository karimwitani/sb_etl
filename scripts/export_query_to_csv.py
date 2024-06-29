import sys
import pandas as pd
from sqlalchemy import create_engine, text

def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def export_to_csv(engine, query, output_file):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        column_names = result.keys()
        rows = result.fetchall()
        df = pd.DataFrame(rows, columns=column_names)
        df.to_csv(output_file, index=False)

def main(sql_file, csv_file):
    # Define the database URL
    DATABASE_URL = "postgresql://karim:mypassword@localhost:5432/sb_data"

    # Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    # Read the SQL query from the file
    query = read_sql_file(sql_file)

    # Define the output file path
    output_file = f"./data/{csv_file}"

    # Export the data to CSV
    export_to_csv(engine, query, output_file)

    print(f"Data exported successfully to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python export_query_to_csv.py <input_sql_file> <output_csv_file>")
        sys.exit(1)

    sql_file = sys.argv[1]
    csv_file = sys.argv[2]

    main(sql_file, csv_file)
