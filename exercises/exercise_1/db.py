import duckdb 
from models import RestaurantList

DB_PATH = "restaurants.duckdb"

def get_connection():
    return duckdb.connect(DB_PATH)

def init_db():
    con = get_connection()
    con.execute(
        """ 
        CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        cuisine VARCHAR,
        price_level VARCHAR, 
        rating DOBLE, 
        short_description VARCHAR,
        opening_hours VARCHAR,
        location VARCHAR
        )
        """
    )
    con.close()

def get_next_id(con) -> int:
    result = con.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM restaurants").fetchone()
    return result[0]

def insert_restaurant(restaurant: RestaurantList) -> int:
    con = get_connection()
    new_id = get_next_id(con)

    con.execute(
        """ 
        INSERT INTO restaurants (
        id, name, cuisine, price_level, rating, 
        short_description, opening_hours, location
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    [
        new_id,
        restaurant.name,
        restaurant.cuisine,
        restaurant.price_level,
        restaurant.rating,
        restaurant.rating,
        restaurant.short_description,
        restaurant.opening_hours,
        restaurant.location,
    ],
    )
    con.close()
    return new_id

def fetch_all_restaurants():
    con = get_connection()
    rows = con.execute(
        """ 
        SELECT id, name, cuisine, price_level, rating, 
        short_description, opening_hours, location
        FROM restaurants
        ORDER BY id DESC
        """
    ).fetchall()
    con.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "cuisine": row[2],
            "price_level": row[3],
            "rating": row[4],
            "short_description": row[5],
            "opening_hours": row[6],
            "location": row[7],
        }
        for row in rows
    ]