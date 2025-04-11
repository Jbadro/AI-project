from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import UserPreferences
from . import db
import json
from .product_data import generate_grocery_list, get_all_grocery_items
from .recommendation import NutritionOptimizer
from .api.walmart import walmart_api

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
    return render_template("profile.html", user=current_user, preferences=preferences)

@views.route('/grocery-list', methods=['GET', 'POST'])
@login_required
def grocery_list():
    preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
    
    if not preferences:
        flash('Please set your preferences first!', category='error')
        return redirect(url_for('views.set_preferences'))
    
    # Use the advanced recommendation system when possible,
    # fallback to simple generation if it fails
    try:
        optimizer = NutritionOptimizer()
        grocery_items = optimizer.optimize_grocery_list(
            diet_type=preferences.diet_type,
            calorie_target=preferences.calorie_target,
            weekly_budget=preferences.budget,
            allergies=preferences.allergies
        )
    except Exception as e:
        # Log the error (in a real app)
        print(f"Recommendation system error: {e}")
        # Fall back to simple recommendation
        grocery_items = generate_grocery_list(
            diet_type=preferences.diet_type,
            calorie_target=preferences.calorie_target,
            weekly_budget=preferences.budget,
            allergies=preferences.allergies
        )
    
    # Calculate totals
    total_price = sum(item["price"] for item in grocery_items)
    # This is daily calories for a single serving of each item
    # In a real app, we would calculate this more accurately based on weekly portions
    total_calories = sum(item["calories"] for item in grocery_items) 
    
    # If user requested to regenerate (POST), we could add randomization here
    if request.method == 'POST':
        # In a real app, we would use ML to provide alternative recommendations
        # For now, we'll just flash a message
        flash('Your grocery list has been regenerated!', category='success')
    
    return render_template(
        "grocery_list.html", 
        user=current_user, 
        grocery_items=grocery_items,
        total_price=total_price,
        total_calories=total_calories
    )

@views.route('/set-preferences', methods=['GET', 'POST'])
@login_required
def set_preferences():
    preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        diet_type = request.form.get('diet_type')
        calorie_target = request.form.get('calorie_target')
        budget = request.form.get('budget')
        allergies = request.form.get('allergies')
        
        if not calorie_target or not budget:
            flash('Please fill in all required fields!', category='error')
        else:
            if preferences:
                preferences.diet_type = diet_type
                preferences.calorie_target = calorie_target
                preferences.budget = budget
                preferences.allergies = allergies
            else:
                new_preferences = UserPreferences(
                    user_id=current_user.id,
                    diet_type=diet_type,
                    calorie_target=calorie_target,
                    budget=budget,
                    allergies=allergies
                )
                db.session.add(new_preferences)
                
            db.session.commit()
            flash('Preferences updated successfully!', category='success')
            return redirect(url_for('views.profile'))
        
    return render_template("preferences.html", user=current_user, preferences=preferences)

@views.route('/product/<int:product_id>')
@login_required
def product_detail(product_id):
    """Display detailed information about a specific product."""
    # Get product details from the API
    product_data = walmart_api.get_product_details(product_id)
    
    if product_data['status'] == 'error':
        flash(product_data['message'], category='error')
        return redirect(url_for('views.grocery_list'))
    
    # Get price history
    price_history = walmart_api.get_price_history(product_id, days=30)
    
    # Get store availability (using a default zip code)
    store_data = walmart_api.get_store_availability(product_id, '90210')
    
    return render_template(
        "product_detail.html",
        user=current_user,
        product=product_data['product'],
        price_history=price_history['priceHistory'] if price_history['status'] == 'success' else [],
        stores=store_data['stores'] if store_data['status'] == 'success' else []
    )

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search_products():
    """Search for products in the Walmart database."""
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    
    results = []
    if query:
        # Search the API
        search_data = walmart_api.search_products(query, category)
        if search_data['status'] == 'success':
            results = search_data['items']
    
    return render_template(
        "search_results.html",
        user=current_user,
        query=query,
        category=category,
        results=results
    )

@views.route('/dashboard')
@login_required
def dashboard():
    """Display nutrition and budget analytics dashboard."""
    preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
    
    if not preferences:
        flash('Please set your preferences first!', category='error')
        return redirect(url_for('views.set_preferences'))
    
    # Get the most recent grocery list (we'll simulate it)
    try:
        optimizer = NutritionOptimizer()
        grocery_items = optimizer.optimize_grocery_list(
            diet_type=preferences.diet_type,
            calorie_target=preferences.calorie_target,
            weekly_budget=preferences.budget,
            allergies=preferences.allergies
        )
    except Exception as e:
        grocery_items = generate_grocery_list(
            diet_type=preferences.diet_type,
            calorie_target=preferences.calorie_target,
            weekly_budget=preferences.budget,
            allergies=preferences.allergies
        )
    
    # Calculate statistics
    total_calories = sum(item["calories"] for item in grocery_items)
    total_protein = sum(item["protein"] for item in grocery_items)
    total_carbs = sum(item["carbs"] for item in grocery_items)
    total_fat = sum(item["fat"] for item in grocery_items)
    total_spent = sum(item["price"] for item in grocery_items)
    
    # Categorize spending
    protein_foods_spending = sum(item["price"] for item in grocery_items if item["category"] in ["meat", "seafood", "dairy"])
    produce_spending = sum(item["price"] for item in grocery_items if item["category"] in ["fruit", "vegetable"])
    other_spending = total_spent - protein_foods_spending - produce_spending
    
    # Calculate dietary compliance
    diet_type_lower = preferences.diet_type.lower() if preferences.diet_type else "no restrictions"
    compliant_items = [item for item in grocery_items if diet_type_lower in [dt.lower() for dt in item.get("diet_types", [])]]
    compliance_percentage = (len(compliant_items) / len(grocery_items)) * 100 if grocery_items else 100
    
    # Determine if allergies are avoided
    allergies_avoided = True
    if preferences.allergies:
        allergens = [a.strip().lower() for a in preferences.allergies.split(',')]
        for item in grocery_items:
            item_name_lower = item["name"].lower()
            if any(allergen in item_name_lower for allergen in allergens):
                allergies_avoided = False
                break
    
    # Generate nutrition recommendations based on stats
    recommendations = []
    
    # Protein recommendation
    protein_target = preferences.calorie_target * 0.15 / 4  # 15% of calories from protein, 4 cal/g
    if total_protein < protein_target:
        recommendations.append({
            "title": "Increase Protein Intake",
            "description": "Your current grocery list provides less protein than recommended. Consider adding more lean meats, fish, eggs, or plant-based protein sources."
        })
    
    # Carbs recommendation
    carbs_target = preferences.calorie_target * 0.55 / 4  # 55% of calories from carbs, 4 cal/g
    if total_carbs < carbs_target and diet_type_lower not in ["keto", "low-carb"]:
        recommendations.append({
            "title": "Add More Complex Carbs",
            "description": "Consider adding more whole grains, fruits, and vegetables to meet your carbohydrate needs for optimal energy."
        })
    elif total_carbs > carbs_target and diet_type_lower in ["keto", "low-carb"]:
        recommendations.append({
            "title": "Reduce Carbohydrates",
            "description": "Your current selections contain more carbs than recommended for your chosen diet. Consider swapping some high-carb items for lower-carb alternatives."
        })
    
    # Budget recommendation
    if total_spent > preferences.budget:
        recommendations.append({
            "title": "Budget Optimization",
            "description": "Your selections exceed your budget. Try replacing some premium items with more affordable alternatives or buying in bulk."
        })
    elif total_spent < preferences.budget * 0.7:
        recommendations.append({
            "title": "Nutrition Boost Opportunity",
            "description": "You're well under budget. Consider adding more nutrient-dense foods to maximize your nutritional intake."
        })
    
    # Add a general recommendation if we have few specific ones
    if len(recommendations) < 2:
        recommendations.append({
            "title": "Balanced Diet Reminder",
            "description": "Remember to include a variety of food groups to ensure you get all essential nutrients, vitamins, and minerals."
        })
    
    # Limit to 3 recommendations
    recommendations = recommendations[:3]
    
    # Format data for the template
    calorie_stats = {
        "current": total_calories,
        "target": preferences.calorie_target
    }
    
    budget_stats = {
        "spent": total_spent,
        "total": preferences.budget
    }
    
    macro_stats = {
        "protein": total_protein,
        "carbs": total_carbs,
        "fat": total_fat,
        "protein_target": protein_target
    }
    
    category_stats = {
        "protein_foods": protein_foods_spending,
        "produce": produce_spending,
        "other": other_spending
    }
    
    dietary_compliance = {
        "diet_type": preferences.diet_type,
        "compliance_percentage": round(compliance_percentage, 1),
        "allergies_avoided": allergies_avoided
    }
    
    return render_template(
        "dashboard.html",
        user=current_user,
        calorie_stats=calorie_stats,
        budget_stats=budget_stats,
        macro_stats=macro_stats,
        category_stats=category_stats,
        dietary_compliance=dietary_compliance,
        recommendations=recommendations
    )

@views.route('/api-docs')
@login_required
def api_docs():
    """Display API documentation."""
    return render_template("api_docs.html", user=current_user)
