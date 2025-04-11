# NutriTech

NutriTech is a personalized grocery list generation application that takes into account an individual's nutritional needs, diet restrictions, and budget constraints.

## Project Overview

Many people struggle with buying groceries that align with their nutritional, diet, and budget constraints. Finding a balance between healthy and affordable food can be tricky, especially with fluctuating grocery prices and available product choices.

NutriTech provides a solution by generating personalized grocery lists based on user preferences. By integrating with product databases, users can access affordable grocery options tailored to their specific needs.

## Features

- **Personalized grocery recommendations** based on:
  - Diet type (vegetarian, vegan, keto, etc.)
  - Calorie targets
  - Budget constraints
  - Food allergies and restrictions

- **User profiles** to store preferences and settings
- **Nutritional analysis** of grocery lists
- **Budget tracking** for grocery expenses

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **ML Components**: Custom recommendation algorithms (expandable to PyTorch/TensorFlow)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Authentication**: Flask-Login

## Setup and Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```
4. Access the application at `http://localhost:5000`

## Project Structure

```
NutriTech/
├── main.py                # Application entry point
├── tests.py               # Unit tests
├── website/
│   ├── __init__.py        # Flask application initialization
│   ├── auth.py            # Authentication routes
│   ├── models.py          # Database models
│   ├── product_data.py    # Grocery items dataset
│   ├── recommendation.py  # ML recommendation system
│   ├── views.py           # Main application routes
│   └── templates/         # HTML templates
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── sign_up.html
│       ├── profile.html
│       ├── preferences.html
│       └── grocery_list.html
```

## Future Enhancements

- Integration with real Walmart API for live product data
- Advanced machine learning models using PyTorch/TensorFlow
- Meal planning and recipe suggestions
- Mobile application
- Grocery delivery integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Authors

- Rosa Shakouri
- Rachelle Falcon
- Muhammad Afan Malik
- Rhakeem Lightbourn
- Jorge Badro

## License

This project is licensed under the MIT License - see the LICENSE file for details.
