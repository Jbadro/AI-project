"""
NutriTech API Endpoints

This module provides API endpoints for interacting with NutriTech functionality.
For this prototype, we use Flask routes to implement a simple REST API.
"""

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from ..recommendation import NutritionOptimizer
from ..product_data import get_all_grocery_items
from ..models import UserPreferences
from .. import db

api = Blueprint('api', __name__)

@api.route('/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """
    Get personalized grocery recommendations based on user preferences.
    
    Query Parameters:
        diet_type (str): Type of diet (optional)
        calorie_target (int): Daily calorie target (optional)
        budget (float): Weekly budget (optional)
        allergies (str): Comma-separated allergies (optional)
        
    Returns:
        JSON response with recommended grocery items
    """
    # Get user preferences from query parameters or from the database
    diet_type = request.args.get('diet_type')
    calorie_target = request.args.get('calorie_target')
    budget = request.args.get('budget')
    allergies = request.args.get('allergies')
    
    # If any parameter is missing, try to get from user preferences
    if not all([diet_type, calorie_target, budget]):
        preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
        if preferences:
            diet_type = diet_type or preferences.diet_type
            calorie_target = calorie_target or preferences.calorie_target
            budget = budget or preferences.budget
            allergies = allergies or preferences.allergies
    
    # Convert string parameters to appropriate types
    try:
        if calorie_target:
            calorie_target = int(calorie_target)
        if budget:
            budget = float(budget)
    except (ValueError, TypeError):
        return jsonify({
            'status': 'error',
            'message': 'Invalid parameter types. calorie_target must be an integer, budget must be a number.'
        }), 400
    
    # Generate recommendations
    try:
        optimizer = NutritionOptimizer()
        recommended_items = optimizer.optimize_grocery_list(
            diet_type=diet_type,
            calorie_target=calorie_target,
            weekly_budget=budget,
            allergies=allergies
        )
        
        # Calculate totals
        total_price = sum(item["price"] for item in recommended_items)
        total_calories = sum(item["calories"] for item in recommended_items)
        total_protein = sum(item["protein"] for item in recommended_items)
        total_carbs = sum(item["carbs"] for item in recommended_items)
        total_fat = sum(item["fat"] for item in recommended_items)
        
        return jsonify({
            'status': 'success',
            'parameters': {
                'diet_type': diet_type,
                'calorie_target': calorie_target,
                'budget': budget,
                'allergies': allergies
            },
            'recommendations': recommended_items,
            'summary': {
                'total_price': total_price,
                'total_calories': total_calories,
                'total_protein': total_protein,
                'total_carbs': total_carbs,
                'total_fat': total_fat,
                'item_count': len(recommended_items)
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error generating recommendations: {str(e)}'
        }), 500

@api.route('/products', methods=['GET'])
@login_required
def get_products():
    """
    Get all available products or filter by criteria.
    
    Query Parameters:
        category (str): Filter by category (optional)
        diet_type (str): Filter by diet type (optional)
        min_price (float): Minimum price (optional)
        max_price (float): Maximum price (optional)
        
    Returns:
        JSON response with product data
    """
    category = request.args.get('category')
    diet_type = request.args.get('diet_type')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    # Get all products
    products = get_all_grocery_items()
    
    # Apply filters
    if category:
        products = [p for p in products if p['category'].lower() == category.lower()]
    
    if diet_type:
        products = [p for p in products if diet_type.lower() in [dt.lower() for dt in p['diet_types']]]
    
    if min_price:
        try:
            min_price = float(min_price)
            products = [p for p in products if p['price'] >= min_price]
        except (ValueError, TypeError):
            pass
    
    if max_price:
        try:
            max_price = float(max_price)
            products = [p for p in products if p['price'] <= max_price]
        except (ValueError, TypeError):
            pass
    
    return jsonify({
        'status': 'success',
        'count': len(products),
        'products': products
    })

@api.route('/preferences', methods=['GET', 'POST', 'PUT'])
@login_required
def manage_preferences():
    """
    Get or update user preferences.
    
    Methods:
        GET: Retrieve current preferences
        POST/PUT: Update preferences
        
    Returns:
        JSON response with preferences data
    """
    if request.method == 'GET':
        # Get current preferences
        preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
        
        if not preferences:
            return jsonify({
                'status': 'error',
                'message': 'No preferences found for this user.'
            }), 404
        
        return jsonify({
            'status': 'success',
            'preferences': {
                'diet_type': preferences.diet_type,
                'calorie_target': preferences.calorie_target,
                'budget': preferences.budget,
                'allergies': preferences.allergies,
                'last_updated': preferences.date_updated.isoformat() if preferences.date_updated else None
            }
        })
    
    elif request.method in ['POST', 'PUT']:
        # Update preferences
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided.'
            }), 400
        
        # Get required fields
        diet_type = data.get('diet_type')
        calorie_target = data.get('calorie_target')
        budget = data.get('budget')
        allergies = data.get('allergies')
        
        # Validate data
        if calorie_target is not None:
            try:
                calorie_target = int(calorie_target)
                if calorie_target <= 0:
                    return jsonify({
                        'status': 'error',
                        'message': 'calorie_target must be a positive integer.'
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    'status': 'error',
                    'message': 'calorie_target must be a positive integer.'
                }), 400
        
        if budget is not None:
            try:
                budget = float(budget)
                if budget <= 0:
                    return jsonify({
                        'status': 'error',
                        'message': 'budget must be a positive number.'
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    'status': 'error',
                    'message': 'budget must be a positive number.'
                }), 400
        
        # Get or create preferences
        preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
        
        if preferences:
            # Update existing preferences
            if diet_type is not None:
                preferences.diet_type = diet_type
            if calorie_target is not None:
                preferences.calorie_target = calorie_target
            if budget is not None:
                preferences.budget = budget
            if allergies is not None:
                preferences.allergies = allergies
        else:
            # Create new preferences
            if not all([diet_type, calorie_target, budget]):
                return jsonify({
                    'status': 'error',
                    'message': 'Missing required fields for new preferences: diet_type, calorie_target, budget.'
                }), 400
            
            preferences = UserPreferences(
                user_id=current_user.id,
                diet_type=diet_type,
                calorie_target=calorie_target,
                budget=budget,
                allergies=allergies or ''
            )
            db.session.add(preferences)
        
        # Commit changes
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Preferences updated successfully.',
            'preferences': {
                'diet_type': preferences.diet_type,
                'calorie_target': preferences.calorie_target,
                'budget': preferences.budget,
                'allergies': preferences.allergies,
                'last_updated': preferences.date_updated.isoformat() if preferences.date_updated else None
            }
        })
    
    # Other methods not allowed
    return jsonify({
        'status': 'error',
        'message': 'Method not allowed.'
    }), 405
