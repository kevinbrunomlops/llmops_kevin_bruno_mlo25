import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Restaurant Generator", layout="centered")
st.title("🍽️ Restaurant Generator")
st.write("Generate and store restaurant based on location and cuisine")

with st.form("restaurant_form"):
    location = st.text_input("Location", placeholder="e.g. Gothenburg city center")
    cuisine = st.text_input("Cuisine", placeholder="e.g. Italian")
    submitted = st.form_submit_button("Generate restaurant")

if submitted:
    if not location or not cuisine:
        st.error("Please enter both location and cuisine.")
    else:
        payload = {"location": location, "cuisine": cuisine}
        try:
            response = requests.post(f"{API_BASE_URL}/restaurants/generate", json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()

            st.success(data["message"])
            restaurant = data["restaurant"]

            st.subheader("Generated restaurant")
            st.write(f"**Name:** {restaurant['name']}")
            st.write(f"**Cuisine:** {restaurant['type_of_food']}")
            st.write(f"**Price level:** {restaurant['price_level']}")
            st.write(f"**Rating:** {restaurant['rating']}")
            st.write(f"**Description:** {restaurant['short_description']}")
            st.write(f"**Opening hours:** {restaurant['opening_hours']}")
            st.write(f"**Location:** {restaurant['location']}")
        except requests.RequestException as e:
            st.error(f"API error: {e}")

st.divider()
st.subheader("Stored restaurants")

if st.button("Refresh restaurant list"):
    try:
        response = requests.get(f"{API_BASE_URL}/restaurants", timeout=30)
        response.raise_for_status()
        restaurants = response.json()

        if restaurants:
            st.dataframe(restaurants, use_container_width=True)
        else:
            st.info("No restaurants stored yet.")
    except requests.RequestException as e:
        st.error(f"Could not fetch restaurants: {e}")