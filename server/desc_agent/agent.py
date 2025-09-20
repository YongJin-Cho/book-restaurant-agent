from pydantic import BaseModel, Field
from typing import List, Optional

class Location(BaseModel):
    lon: float = Field(description="Longitude coordinate")
    lat: float = Field(description="Latitude coordinate")

class Review(BaseModel):
    review: str = Field(description="The review text")
    stars: int = Field(description="Star rating for this review")

class RestaurantInput(BaseModel):
    id: str = Field(description="Unique restaurant identifier")
    name: str = Field(description="Restaurant name")
    address: str = Field(description="Street address")
    city: str = Field(description="City name")
    state: str = Field(description="State abbreviation")
    postal_code: str = Field(description="Postal/ZIP code")
    stars: float = Field(description="Overall star rating")
    review_count: int = Field(description="Total number of reviews")
    categories: Optional[List[str]] = Field(default=None, description="List of restaurant categories. Multiple values allowed. Possible values include: Acai Bowls, American (New), American (Traditional), Argentine, Asian Fusion, Australian, Bagels, Bakeries, Barbeque, Bars, Basque, Beer, Beer Bar, Beer Gardens, Belgian, Brazilian, Breakfast & Brunch, Breweries, Brewpubs, British, Bubble Tea, Buffets, Burgers, Butcher, Cafes, Cafeteria, Cajun/Creole, Cantonese, Caribbean, Caterers, Champagne Bars, Cheese Shops, Chicken Shop, Chicken Wings, Chinese, Cocktail Bars, Coffee & Tea, Coffee Roasteries, Coffeeshops, Comfort Food, Creperies, Cuban, Cupcakes, Delicatessen, Delis, Desserts, Dim Sum, Diners, Dive Bars, Do-It-Yourself Food, Donuts, Empanadas, Ethiopian, Ethnic Food, Ethnic Grocery, Falafel, Farmers Market, Fast Food, Fish & Chips, Fondue, Food Court, Food Delivery Services, Food Stands, Food Tours, Food Trucks, French, Fruits & Veggies, Gastropubs, Gelato, German, Gluten-Free, Greek, Grocery, Halal, Hawaiian, Health Markets, Himalayan/Nepalese, Hookah Bars, Hot Dogs, Hot Pot, Hotels, Ice Cream & Frozen Yogurt, Imported Food, Indian, Indonesian, International Grocery, Irish, Italian, Japanese, Juice Bars & Smoothies, Kebab, Korean, Latin American, Lebanese, Live/Raw Food, Local Flavor, Lounges, Meat Shops, Mediterranean, Mexican, Middle Eastern, Modern European, Moroccan, New Mexican Cuisine, Noodles, Organic Stores, Pakistani, Pasta Shops, Patisserie/Cake Shop, Personal Chefs, Peruvian, Piano Bars, Pizza, Poke, Pop-Up Restaurants, Public Markets, Pubs, Ramen, Salad, Sandwiches, Scandinavian, Seafood, Soul Food, Soup, Southern, Spanish, Speakeasies, Specialty Food, Sports Bars, Steakhouses, Street Vendors, Sushi Bars, Szechuan, Tacos, Tapas Bars, Tapas/Small Plates, Tasting Classes, Tex-Mex, Thai, Themed Cafes, Turkish, Tuscan, Vegan, Vegetarian, Vietnamese, Whiskey Bars, Wine & Spirits, Wine Bars, Wine Tasting Classes, Wine Tasting Room, Wine Tours, Wineries, Wraps. E.g., ['Italian', 'Pizza', 'Wine Bars'] or ['Coffee & Tea', 'Breakfast & Brunch', 'Bakeries']")
    location: Optional[Location] = Field(default=None, description="Geographic coordinates")
    ambiences: Optional[List[str]] = Field(default=None, description="Restaurant ambience descriptors. Multiple values allowed. Possible values: casual, classy, divey, hipster, intimate, romantic, touristy, trendy, upscale. E.g., ['casual', 'trendy'] or ['romantic', 'upscale', 'intimate']")
    good_for_kids: Optional[bool] = Field(default=False, description="Whether the restaurant is kid-friendly")
    has_tv: Optional[bool] = Field(default=False, description="Whether the restaurant has TV")
    good_for_meals: Optional[List[str]] = Field(default=None, description="Meals the restaurant is good for. Multiple values allowed. Possible values: breakfast, brunch, dessert, dinner, latenight, lunch. E.g., ['breakfast', 'brunch'] or ['lunch', 'dinner', 'latenight']")
    dogs_allowed: Optional[bool] = Field(default=False, description="Whether dogs are allowed")
    happy_hour: Optional[bool] = Field(default=False, description="Whether the restaurant offers happy hour")
    parkings: Optional[List[str]] = Field(default=None, description="Available parking options. Multiple values allowed. Possible values: garage, lot, street, valet, validated. E.g., ['street', 'lot'] or ['valet', 'validated']")
    wifi: Optional[bool] = Field(default=False, description="Whether WiFi is available")
    tips: Optional[List[str]] = Field(default=None, description="Customer tips and recommendations")
    reviews: Optional[List[Review]] = Field(default=None, description="Customer reviews with ratings")

from google.adk.agents import Agent

root_agent = Agent(
    name="desc_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are a helpful assistant that analyzes restaurant reviews and tips to create a concise summary.

        Write a one-paragraph description based on the given data, including reviews and tips for the restaurant.
        Focus on the key qualities of the restaurant, including:
        1. The overall atmosphere and vibe.
        2. Specific menu items or dishes that are highly praised or criticized.
        3. The quality of the food and service.
        4. Notable features or unique aspects of the restaurant.

        Please ignore personal anecdotes, irrelevant details (like music choices or individual feelings),
        and simple one-word comments (e.g., "Love it").
        The final output should be a single, coherent paragraph that highlights the restaurant's defining characteristics.
    """,
    input_schema=RestaurantInput,
    include_contents="none"
)