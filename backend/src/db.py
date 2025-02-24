"""File to handle all database-related operations using SQLAlchemy"""
import json
import pandas as pd
from sqlalchemy import create_engine, text

DB_FILE = "sqlite:///bakedbot.db"

def get_engine(db_file):
    """Returns a new database engine instance"""
    return create_engine(db_file, echo=True, connect_args={"check_same_thread": False})

def init_db(engine):
    """Initialize the database with the Mock Data"""
    with engine.connect() as conn:
        conn.begin()
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS ingredients (
                name TEXT PRIMARY KEY,
                properties TEXT NOT NULL,
                common_effects TEXT NOT NULL
            )
        '''))

        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT NOT NULL,
                effects TEXT NOT NULL,         -- JSON String
                ingredients TEXT NOT NULL,     -- JSON String
                price REAL NOT NULL,
                sales_data TEXT NOT NULL       -- JSON String
            )
        '''))

        # conn.execute(text('''
        #     CREATE TABLE IF NOT EXISTS sales (
        #         product_id INTEGER NOT NULL,
        #         date TEXT NOT NULL,
        #         units_sold INTEGER NOT NULL,
        #         FOREIGN KEY (product_id) REFERENCES products(id)
        #     )
        # '''))
        conn.commit()

def convert_columns_to_json(df, columns):
    """Convert specific columns to JSON format for SQLite storage"""
    # print(df[columns].head())
    for column in columns:
        df[column] = df[column].apply(lambda x: json.dumps(eval(x)) if isinstance(x, str) \
                                      and x.startswith("[") else json.dumps(x))

    # print(df[columns].head())
    return df

# def convert_columns_to_json(df, columns):
#     """Convert specific columns to JSON format for SQLite storage"""
#     print("Before Conversion:")
#     print(df[columns].head())  # Print before conversion

#     for column in columns:
#         df[column] = df[column].apply(lambda x: json.dumps(json.loads(x))\
#                                       if isinstance(x, str) else json.dumps(x))

#     print("After Conversion:")
#     print(df[columns].head())  # Print after conversion

#     return df


def fetch_table_data(table_name, engine, mode="default"):
    """Fetches all data from the given table in the specified database
    
    :param table_name: Name of the table to fetch data from.
    :param engine: SQLite database engine.
    :param mode: "default" (returns list of dicts) or "df" (returns pandas DataFrame).
    :return: List of dictionaries (default) or DataFrame if mode="df".
    """
    # engine = get_engine(db_file)
    print("inside fetch table data")

    with engine.connect() as conn:
        conn.begin()
        result = conn.execute(text(f"SELECT * FROM {table_name}"))

        if mode == "df":
            # Convert query result to Pandas DataFrame
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            # engine.dispose()
            conn.commit()
            return df
        else:
            # Default: Convert query result to list of dictionaries
            data = [dict(row) for row in result.mappings()]
            # engine.dispose()
            conn.commit()
            return data

    # engine.dispose()
    return data

def get_list_products(engine, mode="default"):
    """Get product list"""
    # engine = get_engine(db_file)
    # print("inside fetch table data")

    with engine.connect() as conn:
        conn.begin()
        result = conn.execute(text("SELECT * FROM products"))

        if mode == "df":
            # Convert query result to Pandas DataFrame
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            # engine.dispose()
            conn.commit()
            return df
        else:
            data = []
            json_columns = ["effects", "ingredients", "sales_data"]
            for row in result.mappings():
                row_dict = dict(row)  # Convert to dictionary

                # Convert specified JSON columns
                for col in json_columns:
                    if col in row_dict and isinstance(row_dict[col], str):  # Ensure it's a string
                        try:
                            row_dict[col] = json.loads(row_dict[col])  # Convert to Python object
                        except json.JSONDecodeError:
                            pass  # Keep original if conversion fails

                data.append(row_dict)
            return data
    # engine.dispose()
    return data


def get_list_ingrediants(engine, mode="default"):
    """Get Ingredients list"""
    # engine = get_engine(db_file)
    print("inside fetch table data")

    with engine.connect() as conn:
        conn.begin()
        result = conn.execute(text("SELECT * FROM ingredients"))

        if mode == "df":
            # Convert query result to Pandas DataFrame
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            # engine.dispose()
            conn.commit()
            return df
        else:
            data = []
            json_columns = ["common_effects"]
            for row in result.mappings():
                row_dict = dict(row)  # Convert to dictionary

                # Convert specified JSON columns
                for col in json_columns:
                    if col in row_dict and isinstance(row_dict[col], str):  # Ensure it's a string
                        try:
                            row_dict[col] = json.loads(row_dict[col])  # Convert to Python object
                        except json.JSONDecodeError:
                            pass  # Keep original if conversion fails

                data.append(row_dict)
            return data
    # engine.dispose()
    return data


def load_csv_to_db(engine):
    """Load CSV data into SQLite database with JSON column handling"""
    # Read CSV files
    ingredients_df = pd.read_csv("data/Ingredient_Data.csv")
    products_df = pd.read_csv("data/Product_Data.csv")
    # sales_df = pd.read_csv("data/Sales_Data.csv")

    # print(ingredients_df.head())

    # Convert list-like columns to JSON format
    products_df = convert_columns_to_json(products_df, ["effects", "ingredients", "sales_data"])
    ingredients_df = convert_columns_to_json(ingredients_df, ["common_effects"])

    # print(ingredients_df.head())
    # Store data into SQLite
    with engine.connect() as conn:
        conn.begin()
        ingredients_df.to_sql("ingredients", conn, if_exists="append", index=False)
        products_df.to_sql("products", conn, if_exists="replace", index=False)
        # sales_df.to_sql("sales", conn, if_exists="replace", index=False)
        conn.commit()

def get_product_details_by_id(engine, product_id):
    """Fetch a single product from the database by ID."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM products WHERE id = :id"), {"id": product_id})
        row = result.mappings().first()  # Fetch the first row as a dictionary
        if row:
            product = dict(row)  # Convert RowMapping to a dictionary
            # Convert JSON string fields back to Python lists/dicts
            product["effects"] = json.loads(product["effects"])
            product["ingredients"] = json.loads(product["ingredients"])
            # product["sales_data"] = json.loads(product["sales_data"])

            return product

        return product  # Returns None if no product found

# def get_sales_data_by_prod(engine, product_id):
#     """Fetch sales data of a product from the database by ID."""
#     with engine.connect() as conn:
#         result = conn.execute(text("SELECT * FROM sales WHERE product_id = :id"),
#                               {"id": product_id})
#         row = result.mappings().first()  # Fetch the first row as a dictionary
#         if row:
#             sales = dict(row)  # Convert RowMapping to a dictionary
#             return sales
#         return None  # Returns None if no product found


if __name__ == "__main__":
    connection_engine = get_engine(DB_FILE)
    # Should run for first time. !! so uncomment below two lines if running for first time. !!
    init_db(connection_engine)
    load_csv_to_db(connection_engine)
    # ing = fetch_table_data("ingredients", connection_engine, mode="df")
    # prod = fetch_table_data("products", connection_engine, mode="df")
    # sal = fetch_table_data("sales", connection_engine, mode="df")
    # print(ing.head())
    # print(prod.head())
    # print(sal.head())
    connection_engine.dispose()
