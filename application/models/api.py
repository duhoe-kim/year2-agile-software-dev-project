import requests as req

apiKey = "6bb153235fde4d47862b89dabba48ef9"

def get_meal_plans(calories, diet):

    get_meal_plan_URL = f"https://api.spoonacular.com/mealplanner/generate?apiKey={apiKey}"

    timeframe = "day"
    target_calories = calories
    preferred_diet = diet
    meal_plan_query = f"&timeFrame={timeframe}&targetCalories={target_calories}&diet={preferred_diet}"

    url = get_meal_plan_URL + meal_plan_query

    mealPlans = req.get(url)
    
    return mealPlans.json()