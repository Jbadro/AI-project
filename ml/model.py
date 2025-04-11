"""
Machine Learning Model for NutriTech

This module will eventually integrate with PyTorch/TensorFlow for advanced ML capabilities.
For now, it provides a rule-based system that simulates ML behavior.
"""

import numpy as np

class DietRecommendationModel:
    """
    A simple model to recommend grocery items based on user preferences.
    
    This is a placeholder for a more sophisticated ML model that would be
    implemented using PyTorch or TensorFlow in the future.
    """
    
    def __init__(self):
        """Initialize the model with default parameters."""
        # Diet type coefficients (simulating trained weights)
        self.diet_coefficients = {
            'vegetarian': np.array([0.8, 1.2, 0.5, 0.0, 1.5]),  # Weights for [protein, carbs, fat, price, nutrition]
            'vegan': np.array([0.7, 1.3, 0.4, 0.0, 1.6]),
            'keto': np.array([1.5, 0.3, 1.8, 0.0, 1.0]),
            'paleo': np.array([1.4, 0.6, 1.2, 0.0, 1.3]),
            'gluten-free': np.array([1.0, 0.9, 1.0, 0.0, 1.2]),
            'low-carb': np.array([1.3, 0.4, 1.4, 0.0, 1.1]),
            'low-fat': np.array([1.2, 1.3, 0.3, 0.0, 1.4]),
            'no restrictions': np.array([1.0, 1.0, 1.0, 0.0, 1.0])
        }
        
        # Budget sensitivity parameters (simulation)
        self.budget_sensitivity = {
            'low': 1.5,      # More sensitive to price
            'medium': 1.0,   # Balanced
            'high': 0.5      # Less sensitive to price
        }
    
    def predict_item_score(self, item, user_preferences):
        """
        Predict how well an item fits a user's preferences.
        
        Args:
            item (dict): Grocery item with nutritional information
            user_preferences (dict): User dietary preferences
            
        Returns:
            float: Score indicating how well the item matches preferences
        """
        diet_type = user_preferences.get('diet_type', 'no restrictions').lower()
        if diet_type not in self.diet_coefficients:
            diet_type = 'no restrictions'
            
        # Get diet coefficients
        coeffs = self.diet_coefficients[diet_type]
        
        # Budget sensitivity (default to medium)
        budget = user_preferences.get('budget', 100)
        budget_level = 'medium'
        if budget < 50:
            budget_level = 'low'
        elif budget > 150:
            budget_level = 'high'
        
        budget_coeff = self.budget_sensitivity[budget_level]
        
        # Create feature vector for the item
        features = np.array([
            item['protein'] / 30.0,  # Normalize protein (assuming max ~30g)
            item['carbs'] / 50.0,    # Normalize carbs (assuming max ~50g)
            item['fat'] / 20.0,      # Normalize fat (assuming max ~20g)
            item['price'] / 10.0,    # Normalize price (assuming max ~$10)
            1.0                      # Nutrition constant
        ])
        
        # Apply price sensitivity to price coefficient
        coeffs[3] = -budget_coeff  # Negative because lower price is better
        
        # Calculate score (dot product of features and coefficients)
        score = np.dot(features, coeffs)
        
        # Apply dietary restrictions
        if diet_type in item.get('diet_types', []):
            score *= 1.25  # Boost score for compatible items
        
        # Apply allergy penalties
        allergies = user_preferences.get('allergies', '')
        if allergies:
            allergens = [a.strip().lower() for a in allergies.split(',')]
            for allergen in allergens:
                if allergen in item['name'].lower():
                    score = 0  # Zero score for items with allergens
        
        return float(score)
    
    def recommend_items(self, items, user_preferences, top_n=20):
        """
        Recommend items based on user preferences.
        
        Args:
            items (list): List of grocery items
            user_preferences (dict): User dietary preferences
            top_n (int): Number of items to recommend
            
        Returns:
            list: Recommended items sorted by score
        """
        # Calculate scores for all items
        for item in items:
            item['score'] = self.predict_item_score(item, user_preferences)
        
        # Sort by score (descending)
        recommended_items = sorted(items, key=lambda x: x['score'], reverse=True)
        
        # Take top N items
        recommended_items = recommended_items[:top_n]
        
        # Remove score field before returning
        for item in recommended_items:
            del item['score']
        
        return recommended_items
    
    def optimize_for_budget(self, recommended_items, budget):
        """
        Optimize the recommended items to fit within a budget.
        
        Args:
            recommended_items (list): List of recommended items
            budget (float): Budget constraint
            
        Returns:
            list: Optimized list of items fitting within budget
        """
        if not recommended_items:
            return []
            
        # Sort by value (protein per dollar)
        sorted_items = sorted(
            recommended_items, 
            key=lambda x: (x['protein'] + x['calories']/100) / max(0.01, x['price']), 
            reverse=True
        )
        
        # Greedy algorithm to select items within budget
        selected_items = []
        total_cost = 0
        
        for item in sorted_items:
            if total_cost + item['price'] <= budget:
                selected_items.append(item)
                total_cost += item['price']
        
        return selected_items
