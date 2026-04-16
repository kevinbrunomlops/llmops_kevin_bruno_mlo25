from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from models import RestaurantRequest, RestaurantResponse, RestaurantRow
from agent import generate_restaurant
from db import init_db, insert_restaurant, fetch_all_restaurants

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Restaurant Generator API",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "Restaurant Generator API is running"}

@app.post("/restaurants/generate", response_model=RestaurantResponse)
def create_restaurant(request: RestaurantRequest):
    try:
        print("Incoming request:", request)

        restaurant = generate_restaurant(
            location=request.location,
            cuisine=request.cuisine,
        )
        print("Generated restaurant:", restaurant)

        insert_restaurant(restaurant)

        return RestaurantResponse(
            message="Restaurant generated and stored succesfully",
            restaurant=restaurant,
        )
    except Exception as e:
        print("ERROR in create_restaurant:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/restaurants", response_model=list[RestaurantRow])
def get_restaurants():
    try:
        return fetch_all_restaurants()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))