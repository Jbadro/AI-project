"""
Walmart API Integration Module

In a production environment, this would connect to the actual Walmart Open API.
For this prototype, we simulate the API with mock data.
"""

import json
import random
import time
from datetime import datetime
from ..product_data import grocery_items

class WalmartAPI:
    """
    A class to interact with the Walmart API for grocery data.
    
    This is a simulation of the API for prototype purposes. In production,
    this would make actual HTTP requests to Walmart's Open API endpoints.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the Walmart API client.
        
        Args:
            api_key (str, optional): API key for authentication (not used in simulation)
        """
        self.api_key = api_key or "SIMULATED_API_KEY"
        self.base_url = "https://api.walmart.com/v4" # Simulated base URL
        self.cache = {}
        self.cache_expiry = 3600  # 1 hour cache expiry
    
    def search_products(self, query, category=None, limit=20):
        """
        Search for products in the Walmart database.
        
        Args:
            query (str): Search query
            category (str, optional): Product category
            limit (int, optional): Maximum number of results to return
            
        Returns:
            dict: Search results
        """
        # Simulate API latency
        time.sleep(0.2)
        
        # Cache key
        cache_key = f"search_{query}_{category}_{limit}"
        
        # Check cache
        if cache_key in self.cache:
            cache_time, cache_data = self.cache[cache_key]
            if (datetime.now().timestamp() - cache_time) < self.cache_expiry:
                return cache_data
        
        # Simulate search results
        query = query.lower()
        results = []
        
        for item in grocery_items:
            # Match by name or category
            name_match = query in item['name'].lower()
            category_match = category and category.lower() == item['category'].lower()
            
            if name_match or (category and category_match):
                # Format item as API response
                results.append({
                    'id': item['id'],
                    'name': item['name'],
                    'price': {
                        'amount': item['price'],
                        'currency': 'USD'
                    },
                    'nutritionFacts': {
                        'calories': item['calories'],
                        'protein': item['protein'],
                        'carbohydrates': item['carbs'],
                        'fat': item['fat']
                    },
                    'category': item['category'],
                    'store': item['store'],
                    'dietaryAttributes': item['diet_types'],
                    'imageUrl': f"https://example.com/images/products/{item['id']}.jpg",
                    'inStock': random.choice([True, True, True, False])  # 75% chance of being in stock
                })
        
        # Sort by relevance (simulated)
        results = sorted(results, key=lambda x: 2 if query in x['name'].lower() else 1, reverse=True)
        
        # Limit results
        results = results[:limit]
        
        # Format response
        response = {
            'status': 'success',
            'totalCount': len(results),
            'items': results,
            'timestamp': datetime.now().isoformat()
        }
        
        # Cache results
        self.cache[cache_key] = (datetime.now().timestamp(), response)
        
        return response
    
    def get_product_details(self, product_id):
        """
        Get detailed information about a specific product.
        
        Args:
            product_id (int): Product ID
            
        Returns:
            dict: Product details
        """
        # Simulate API latency
        time.sleep(0.1)
        
        # Cache key
        cache_key = f"product_{product_id}"
        
        # Check cache
        if cache_key in self.cache:
            cache_time, cache_data = self.cache[cache_key]
            if (datetime.now().timestamp() - cache_time) < self.cache_expiry:
                return cache_data
        
        # Find the product
        product = None
        for item in grocery_items:
            if item['id'] == product_id:
                product = item
                break
        
        if not product:
            return {
                'status': 'error',
                'message': f"Product with ID {product_id} not found",
                'timestamp': datetime.now().isoformat()
            }
        
        # Format as API response
        response = {
            'status': 'success',
            'product': {
                'id': product['id'],
                'name': product['name'],
                'price': {
                    'amount': product['price'],
                    'currency': 'USD',
                    'unit': 'each'
                },
                'nutritionFacts': {
                    'calories': product['calories'],
                    'protein': product['protein'],
                    'carbohydrates': product['carbs'],
                    'fat': product['fat'],
                    'servingSize': '1 serving',
                    'servingsPerContainer': random.randint(1, 8)
                },
                'ingredients': 'Simulated ingredients list',
                'category': product['category'],
                'store': product['store'],
                'dietaryAttributes': product['diet_types'],
                'imageUrl': f"https://example.com/images/products/{product['id']}.jpg",
                'inStock': random.choice([True, True, True, False]),  # 75% chance of being in stock
                'quantity': random.randint(1, 50),  # Random stock quantity
                'popularity': random.randint(1, 100),  # Random popularity score
                'customerRating': round(3.5 + random.random() * 1.5, 1),  # Random rating between 3.5 and 5.0
                'reviews': []  # Would contain customer reviews in a real API
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Cache result
        self.cache[cache_key] = (datetime.now().timestamp(), response)
        
        return response
    
    def get_store_availability(self, product_id, zip_code):
        """
        Check if a product is available in stores near a given location.
        
        Args:
            product_id (int): Product ID
            zip_code (str): ZIP code for location
            
        Returns:
            dict: Store availability information
        """
        # Simulate API latency
        time.sleep(0.3)
        
        # Find the product
        product = None
        for item in grocery_items:
            if item['id'] == product_id:
                product = item
                break
        
        if not product:
            return {
                'status': 'error',
                'message': f"Product with ID {product_id} not found",
                'timestamp': datetime.now().isoformat()
            }
        
        # Simulate store data
        stores = [
            {
                'id': 1234,
                'name': 'Walmart Supercenter',
                'address': '123 Main St, Anytown, USA',
                'distance': 2.4,
                'inStock': True,
                'quantity': random.randint(5, 30)
            },
            {
                'id': 5678,
                'name': 'Walmart Neighborhood Market',
                'address': '456 Oak Ave, Anytown, USA',
                'distance': 4.7,
                'inStock': random.choice([True, False]),
                'quantity': random.randint(0, 15)
            },
            {
                'id': 9012,
                'name': 'Walmart Express',
                'address': '789 Pine Blvd, Anytown, USA',
                'distance': 7.2,
                'inStock': random.choice([True, False]),
                'quantity': random.randint(0, 10)
            }
        ]
        
        return {
            'status': 'success',
            'product': {
                'id': product['id'],
                'name': product['name']
            },
            'location': {
                'zipCode': zip_code,
                'city': 'Anytown',
                'state': 'CA'
            },
            'stores': stores,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_price_history(self, product_id, days=30):
        """
        Get historical price data for a product.
        
        Args:
            product_id (int): Product ID
            days (int, optional): Number of days of history to retrieve
            
        Returns:
            dict: Price history data
        """
        # Find the product
        product = None
        for item in grocery_items:
            if item['id'] == product_id:
                product = item
                break
        
        if not product:
            return {
                'status': 'error',
                'message': f"Product with ID {product_id} not found",
                'timestamp': datetime.now().isoformat()
            }
        
        # Generate simulated price history
        current_price = product['price']
        history = []
        
        for i in range(days):
            # Random price fluctuation within 20% of current price
            price_delta = current_price * (random.random() * 0.2 - 0.1)
            day_price = round(current_price + price_delta, 2)
            
            # Ensure price is not negative
            day_price = max(0.01, day_price)
            
            # Calculate date (days ago)
            days_ago = days - i
            
            history.append({
                'date': (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() - days_ago * 86400) * 1000,
                'price': day_price
            })
        
        # Sort by date (ascending)
        history = sorted(history, key=lambda x: x['date'])
        
        return {
            'status': 'success',
            'product': {
                'id': product['id'],
                'name': product['name'],
                'currentPrice': current_price
            },
            'priceHistory': history,
            'timestamp': datetime.now().isoformat()
        }

# Initialize the API client
walmart_api = WalmartAPI()
