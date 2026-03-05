import random

# Generates a random integer number between num1 and num2
def generate_number(num1: int, num2: int):
    if not isinstance(num1, int):
        raise ValueError("Invalid input. Must be an integer.")
    if not isinstance(num2, int):
        raise ValueError("Invalid input. Must be an integer.")

    return random.randint(num1, num2)