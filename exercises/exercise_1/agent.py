from pydantic_ai import Agent
from models import RestaurantList

restaurant_searcher_agent = Agent(
    "openrouter:nvidia/nemotron-3-super-120b-a12b:free",
    system_prompt=""" 
You are a restaurant recommendation assistant. 
The user gives you a location.
Return exactly 5 restaurants near that place. 
It is allowed to invent restaurant if needed, 
but they should still look realistic and relevant to the location.
Vary cuisine types.
Keep descriptions short and useful.
Ratings must be between 1 and 5.
Price level must be one of: $, $$, $$$, $$$$.

""", output_type=RestaurantList
)

def generate_restaurant(location: str, cuisine: str) -> RestaurantList: 
    prompt = (
        f"Create one realistric restaurant for this request.\n"
        f"Location: {location}\n"
        f"Cuisine: {cuisine}"
    )
    result = restaurant_searcher_agent.run_sync(prompt)
    return result.output