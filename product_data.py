"""
Module for interacting with grocery product data.
In a production environment, this would connect to the Walmart API.
For this prototype, we'll use mock data.
"""

# Mock database of grocery items with nutritional information
grocery_items = [
    {
        "id": 1,
        "name": "Organic Bananas (bunch)",
        "price": 2.99,
        "calories": 105,
        "protein": 1.3,
        "carbs": 27.0,
        "fat": 0.4,
        "category": "fruit",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "gluten-free", "low-fat"]
    },
    {
        "id": 2,
        "name": "Chicken Breast (1 lb)",
        "price": 8.99,
        "calories": 165,
        "protein": 31.0,
        "carbs": 0.0,
        "fat": 3.6,
        "category": "meat",
        "store": "Walmart",
        "diet_types": ["keto", "paleo", "low-carb", "gluten-free"]
    },
    {
        "id": 3,
        "name": "Brown Rice (2 lb bag)",
        "price": 3.49,
        "calories": 216,
        "protein": 5.0,
        "carbs": 45.0,
        "fat": 1.8,
        "category": "grain",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "gluten-free"]
    },
    {
        "id": 4,
        "name": "Spinach (10 oz bag)",
        "price": 2.99,
        "calories": 23,
        "protein": 2.9,
        "carbs": 3.6,
        "fat": 0.4,
        "category": "vegetable",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "keto", "paleo", "gluten-free", "low-carb", "low-fat"]
    },
    {
        "id": 5,
        "name": "Eggs (1 dozen)",
        "price": 4.29,
        "calories": 72,
        "protein": 6.3,
        "carbs": 0.4,
        "fat": 5.0,
        "category": "dairy",
        "store": "Walmart",
        "diet_types": ["vegetarian", "keto", "paleo", "gluten-free", "low-carb"]
    },
    {
        "id": 6,
        "name": "Almond Milk (1/2 gallon)",
        "price": 3.99,
        "calories": 30,
        "protein": 1.0,
        "carbs": 1.0,
        "fat": 2.5,
        "category": "dairy_alternative",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "keto", "paleo", "gluten-free", "low-carb", "low-fat"]
    },
    {
        "id": 7,
        "name": "Ground Beef (1 lb)",
        "price": 7.99,
        "calories": 231,
        "protein": 26.0,
        "carbs": 0.0,
        "fat": 15.0,
        "category": "meat",
        "store": "Walmart",
        "diet_types": ["keto", "paleo", "low-carb"]
    },
    {
        "id": 8,
        "name": "Sweet Potatoes (3 lb bag)",
        "price": 3.99,
        "calories": 115,
        "protein": 2.1,
        "carbs": 27.0,
        "fat": 0.1,
        "category": "vegetable",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "paleo", "gluten-free"]
    },
    {
        "id": 9,
        "name": "Greek Yogurt (32 oz)",
        "price": 5.49,
        "calories": 100,
        "protein": 18.0,
        "carbs": 6.0,
        "fat": 0.0,
        "category": "dairy",
        "store": "Walmart",
        "diet_types": ["vegetarian", "gluten-free", "low-fat"]
    },
    {
        "id": 10,
        "name": "Quinoa (16 oz)",
        "price": 4.99,
        "calories": 120,
        "protein": 4.0,
        "carbs": 21.0,
        "fat": 1.9,
        "category": "grain",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "gluten-free"]
    },
    {
        "id": 11,
        "name": "Avocado (each)",
        "price": 1.49,
        "calories": 240,
        "protein": 3.0,
        "carbs": 12.0,
        "fat": 22.0,
        "category": "fruit",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "keto", "paleo", "gluten-free", "low-carb"]
    },
    {
        "id": 12,
        "name": "Canned Tuna (5 oz)",
        "price": 1.29,
        "calories": 70,
        "protein": 16.0,
        "carbs": 0.0,
        "fat": 1.0,
        "category": "canned_goods",
        "store": "Walmart",
        "diet_types": ["keto", "paleo", "gluten-free", "low-carb", "low-fat"]
    },
    {
        "id": 13,
        "name": "Olive Oil (16.9 oz)",
        "price": 7.99,
        "calories": 119,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 14.0,
        "category": "oil",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "keto", "paleo", "gluten-free", "low-carb"]
    },
    {
        "id": 14,
        "name": "Black Beans (15 oz can)",
        "price": 0.99,
        "calories": 110,
        "protein": 7.0,
        "carbs": 20.0,
        "fat": 0.5,
        "category": "canned_goods",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "gluten-free", "low-fat"]
    },
    {
        "id": 15,
        "name": "Broccoli (1 bunch)",
        "price": 2.49,
        "calories": 30,
        "protein": 2.5,
        "carbs": 6.0,
        "fat": 0.3,
        "category": "vegetable",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "keto", "paleo", "gluten-free", "low-carb", "low-fat"]
    },
    {
        "id": 16,
        "name": "Whole Wheat Bread (20 oz loaf)",
        "price": 3.29,
        "calories": 80,
        "protein": 4.0,
        "carbs": 15.0,
        "fat": 1.0,
        "category": "bakery",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "low-fat"]
    },
    {
        "id": 17,
        "name": "Salmon Fillet (1 lb)",
        "price": 12.99,
        "calories": 208,
        "protein": 20.0,
        "carbs": 0.0,
        "fat": 13.0,
        "category": "seafood",
        "store": "Walmart",
        "diet_types": ["keto", "paleo", "gluten-free", "low-carb"]
    },
    {
        "id": 18,
        "name": "Tofu (14 oz)",
        "price": 2.49,
        "calories": 94,
        "protein": 10.0,
        "carbs": 2.0,
        "fat": 6.0,
        "category": "vegetarian_protein",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "gluten-free", "low-carb"]
    },
    {
        "id": 19,
        "name": "Almonds (16 oz)",
        "price": 6.99,
        "calories": 164,
        "protein": 6.0,
        "carbs": 6.0,
        "fat": 14.0,
        "category": "nuts",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "keto", "paleo", "gluten-free", "low-carb"]
    },
    {
        "id": 20,
        "name": "Oatmeal (42 oz)",
        "price": 3.99,
        "calories": 150,
        "protein": 5.0,
        "carbs": 27.0,
        "fat": 3.0,
        "category": "breakfast",
        "store": "Walmart",
        "diet_types": ["vegetarian", "vegan", "low-fat"]
    }
]

def get_all_grocery_items():
    """Return all grocery items in the database."""
    return grocery_items

def filter_by_diet(items, diet_type):
    """Filter grocery items by diet type."""
    if not diet_type or diet_type.lower() == "no restrictions":
        return items
    
    filtered_items = []
    diet_type = diet_type.lower()
    
    for item in items:
        if diet_type in [dt.lower() for dt in item["diet_types"]]:
            filtered_items.append(item)
    
    return filtered_items

def filter_by_allergies(items, allergies_str):
    """Filter out grocery items containing allergens."""
    if not allergies_str:
        return items
    
    # Parse allergies from comma-separated string
    allergies = [a.strip().lower() for a in allergies_str.split(',')]
    
    # Very basic filtering - in a real app, this would be more sophisticated
    filtered_items = []
    for item in items:
        allergen_found = False
        for allergen in allergies:
            # Very simplistic check - would need a proper allergen database
            if allergen in item["name"].lower():
                allergen_found = True
                break
        
        if not allergen_found:
            filtered_items.append(item)
    
    return filtered_items

def filter_by_budget(items, weekly_budget):
    """
    Filter grocery items to fit within a weekly budget.
    This is a simplified implementation - a real algorithm would be more sophisticated.
    """
    if not weekly_budget or weekly_budget <= 0:
        return items
    
    # Sort items by nutrition/price value (simplified)
    sorted_items = sorted(items, key=lambda x: (x["protein"] + x["calories"]/100) / x["price"], reverse=True)
    
    selected_items = []
    total_cost = 0
    
    for item in sorted_items:
        if total_cost + item["price"] <= weekly_budget:
            selected_items.append(item)
            total_cost += item["price"]
    
    return selected_items

def generate_grocery_list(diet_type=None, calorie_target=2000, weekly_budget=100, allergies=None):
    """
    Generate a personalized grocery list based on preferences.
    
    Args:
        diet_type (str): The type of diet (e.g., "vegan", "keto")
        calorie_target (int): Daily calorie target
        weekly_budget (float): Weekly grocery budget
        allergies (str): Comma-separated list of allergies/restrictions
        
    Returns:
        list: List of recommended grocery items
    """
    # Get all items
    items = get_all_grocery_items()
    
    # Apply diet filter
    items = filter_by_diet(items, diet_type)
    
    # Filter out allergens
    items = filter_by_allergies(items, allergies)
    
    # Apply budget constraints
    items = filter_by_budget(items, weekly_budget)
    
    # In a real app, we would use ML to optimize for calorie target and nutrition
    # For now, we'll return the filtered list
    
    return items
