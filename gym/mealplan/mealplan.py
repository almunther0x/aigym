import numpy as np


calories = np.array([option['calories'] for option in meal_options])

# Element (i, j) == True iff meal i has meal type j, and False otherwise.
meal_types = np.empty((len(meal_options), len(MEAL_TYPES)), dtype=bool)

for i, option in enumerate(meal_options):
    for j, meal_type in enumerate(MEAL_TYPES):
        meal_types[i, j] = meal_type in option['types']
        
def make_random_meal_options():
    options = []

    for _ in range(100_000):
        calories = np.random.randint(100, 1_000)
        num_types = np.random.randint(1, len(MEAL_TYPES))
        types = np.random.choice(MEAL_TYPES, num_types, replace=False)

        options.append(dict(calories=calories, types=types))

    # List of dictionaries with keys 'calories' and 'types'
    return options

