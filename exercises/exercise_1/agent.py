from pydantic_ai import Agent
from models import RestaurantSearcher
from dotenv import load_dotenv
from constants import MODEL_LARGE
load_dotenv()

restaurant_searcher_agent = Agent(
    model=MODEL_LARGE,
    system_prompt=""" 
    You generate exactly one restaurant based on the user's location and desired cuisine. 
    Return the fields: name, type_of_food, price_level, rating, 
    short_description, opening_hours, and location.

""", output_type=RestaurantSearcher
)

def generate_restaurant(location: str, cuisine: str) -> RestaurantSearcher: 
    prompt = (
        f"Create one realistric restaurant for this request.\n"
        f"Location: {location}\n"
        f"Cuisine: {cuisine}"
    )
    result = restaurant_searcher_agent.run_sync(prompt)
    return result.output