"""
NutriTech ML Recommendation System

This module contains the core machine learning components for generating 
personalized grocery recommendations based on user preferences.

In a production environment, this would use advanced ML algorithms. 
For this prototype, we implement a rule-based system that will later be
extended with proper ML models.
"""

import numpy as np
from .product_data import get_all_grocery_items
from .ml.model import DietRecommendationModel

class NutritionOptimizer:
    """
    Class for optimizing grocery recommendations based on nutritional needs.
    This is a placeholder for the ML model that would be implemented.
    """
    
    def __init__(self):
        """Initialize the optimizer with default parameters."""
        self.items = get_all_grocery_items()
        
        # Default macronutrient ratios (protein/carbs/fat)
        self.macro_ratios = {
            'balanced': [0.3, 0.4, 0.3],
            'keto': [0.25, 0.05, 0.7],
            'low-carb': [0.35, 0.15, 0.5],
            'high-protein': [0.4, 0.4, 0.2],
            'low-fat': [0.3, 0.6, 0.1],
            'vegan': [0.25, 0.55, 0.2],
            'paleo': [0.3, 0.35, 0.35]
        }
    
    def _calculate_item_score(self, item, diet_type, calorie_target):
        """
        Calculate a score for each item based on how well it fits the user's needs.
        Higher score means better fit.
        
        This is a simplified version - a real ML model would be much more sophisticated.
        """
        score = 0
        
        # Base score - nutrient density per dollar
        protein_per_dollar = item['protein'] / item['price']
        calories_per_dollar = item['calories'] / item['price']
        
        score += protein_per_dollar * 5  # Protein is weighted higher
        score += calories_per_dollar * 0.05
        
        # Diet type adjustment
        if diet_type and diet_type.lower() != 'no restrictions':
            diet_type = diet_type.lower()
            if diet_type in [dt.lower() for dt in item['diet_types']]:
                score *= 1.5  # Boost score for items matching diet type
            else:
                score *= 0.5  # Reduce score for non-matching items
        
        # Macronutrient balance adjustment
        if diet_type and diet_type.lower() in self.macro_ratios:
            ideal_ratios = self.macro_ratios[diet_type.lower()]
            
            # Calculate total macros in this item
            total_macros = item['protein'] + item['carbs'] + item['fat']
            if total_macros > 0:
                # Calculate actual ratios in this item
                actual_ratios = [
                    item['protein'] / total_macros,
                    item['carbs'] / total_macros,
                    item['fat'] / total_macros
                ]
                
                # Calculate difference from ideal ratios
                ratio_diff = sum(abs(a - i) for a, i in zip(actual_ratios, ideal_ratios))
                
                # Adjust score based on how closely item matches ideal macronutrient ratios
                score *= (1 - ratio_diff / 2)  # Penalty for difference from ideal
        
        return score
    
    def optimize_grocery_list(self, diet_type, calorie_target, weekly_budget, allergies=None):
        """
        Generate an optimized grocery list based on user parameters.
        
        Args:
            diet_type (str): User's diet type (e.g., "keto", "vegan")
            calorie_target (int): Daily calorie target
            weekly_budget (float): Weekly grocery budget
            allergies (str): Comma-separated allergies
            
        Returns:
            list: Optimized list of grocery items
        """
        # Use the ML model for more advanced recommendations
        try:
            model = DietRecommendationModel()
            
            # Create user preferences dictionary
            user_preferences = {
                'diet_type': diet_type,
                'calorie_target': calorie_target,
                'budget': weekly_budget,
                'allergies': allergies
            }
            
            # Get initial recommendations
            recommended_items = model.recommend_items(self.items.copy(), user_preferences)
            
            # Optimize for budget
            selected_items = model.optimize_for_budget(recommended_items, weekly_budget)
            
            return selected_items
            
        except Exception as e:
            # Fall back to basic approach if ML model fails
            print(f"ML model error: {e}. Falling back to basic recommendation.")
            
            # For fallback, we'll use a simple greedy approach
            items = self.items.copy()
            
            # Filter out items with allergens
            if allergies:
                allergens = [a.strip().lower() for a in allergies.split(',')]
                items = [item for item in items if not any(a in item['name'].lower() for a in allergens)]
            
            # Calculate scores for each item
            for item in items:
                item['score'] = self._calculate_item_score(item, diet_type, calorie_target)
            
            # Sort items by score
            items.sort(key=lambda x: x['score'], reverse=True)
            
            # Select items within budget
            selected_items = []
            total_cost = 0
            
            for item in items:
                if total_cost + item['price'] <= weekly_budget:
                    selected_items.append(item)
                    total_cost += item['price']
            
            # Remove the score attribute before returning
            for item in selected_items:
                del item['score']
            
            return selected_items

# In a future implementation, we could add more ML components:
# 1. Collaborative filtering based on what similar users purchased
# 2. Neural networks to predict optimal meal combinations
# 3. Reinforcement learning to improve recommendations over time
