import dotenv
dotenv.load_dotenv()

from agent import root_agent
from agent import RestaurantInput

import os
import json

input_json_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "yelp", "restaurant.json")
with open(input_json_file_path, 'r', encoding='utf-8') as file:
    restaurants = json.load(file)

input_json_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "yelp", "restaurant_tips.json")
with open(input_json_file_path, 'r', encoding='utf-8') as file:
    restaurant_tips = json.load(file)

input_json_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "yelp", "restaurant_reviews.json")
with open(input_json_file_path, 'r', encoding='utf-8') as file:
    restaurant_reviews = json.load(file)

for restaurant in restaurants:
    restaurant_id = restaurant.get('id', restaurant.get('business_id'))
    tips_entry = next((item for item in restaurant_tips if item['id'] == restaurant_id), None)
    reviews_entry = next((item for item in restaurant_reviews if item['id'] == restaurant_id), None)
    
    if tips_entry:
        restaurant["tips"] = tips_entry.get("tips", [])
    
    if reviews_entry:
        restaurant["reviews"] = reviews_entry.get("reviews", [])

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import UserContent

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)
    session = await runner.session_service.create_session(app_name=runner.app_name, user_id="user1")

    for count, restaurant in enumerate(restaurants, start=1):
        print(f"Processing restaurant {count}: {restaurant['name']}")

        events = list(runner.run(user_id=session.user_id, session_id=session.id,
                                 new_message=UserContent(RestaurantInput(**restaurant).model_dump_json())))

        restaurant["description"] = events[-1].content.parts[0].text
        print(restaurant["description"])

    for restaurant in restaurants:
        keys_to_keep = {"id", "description"}
        keys_to_remove = [key for key in restaurant.keys() if key not in keys_to_keep]

        for key in keys_to_remove:
            restaurant.pop(key, None)

    output_json_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "yelp", "restaurant_desc.json")
    with open(output_json_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(restaurants, outfile, ensure_ascii=False, indent=2)

asyncio.run(main())
