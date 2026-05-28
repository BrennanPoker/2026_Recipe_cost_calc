import pandas
from tabulate import tabulate


# Functions go here
def make_statement(statement, decoration):
    """Emphasizes heading by adding decoration"""

    # Returns formatted heading
    return f"\n{decoration * 3} {statement} {decoration * 3}\n"


def not_blank(question):
    """Checks that a user response is not blank"""

    while True:

        # Ask user for input
        response = input(question)

        # Check response is not blank
        if response != "":
            return response

        # Error message if input is blank
        print("Sorry, this can't be blank. Please try again.\n")


def num_check(question, num_type="float"):
    """Checks that response is a float / integer more than zero"""

    # Set error message depending on datatype
    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:
        try:

            # Convert response to float or integer
            if num_type == "float":
                response = float(input(question))
            else:
                response = int(input(question))

            # Check number is greater than zero
            if response > 0:
                return response
            else:
                print(error)

        # Runs if input is not a valid number
        except ValueError:
            print(error)


def get_ingredients():
    """Gets ingredient data with validation"""

    # Lists for dataframe
    all_names = []
    all_types = []
    amount_bought_list = []
    amount_needed_list = []

    # Dictionary for dataframe
    ingredient_dict = {
        "Ingredient": all_names,
        "Type": all_types,
        "Amount Bought": amount_bought_list,
        "Amount Needed": amount_needed_list
    }

    # Ingredient loop
    while True:

        # Ask user for ingredient name
        name = not_blank("Ingredient name (or 'xxx' to stop): ")

        # Check user has entered at least one ingredient
        if name == "xxx" and len(all_names) == 0:
            print("You must enter at least one ingredient.\n")
            continue

        # Exit loop if user enters xxx
        elif name == "xxx":
            break

        # Ask user for ingredient type
        while True:
            ing_type = input("Type (whole / liquid / solid): ").lower()

            # Check type is valid
            if ing_type in ["whole", "liquid", "solid"]:
                break

            # Error message for invalid type
            else:
                print("Please choose 'whole', 'liquid', or 'solid'.\n")

        # whole ingredients
        if ing_type == "whole":

            # Whole ingredients are integers
            needed = num_check("How many needed? ", "integer")

            while True:
                bought = num_check("How many bought? ", "integer")

                # Prevent amount bought being smaller than amount needed
                if bought >= needed:
                    break

                else:
                    print("Amount bought cannot be smaller than amount needed.\n")

        # liquid ingredients
        elif ing_type == "liquid":

            # Ask user for liquid unit
            unit = input("Unit (ml / L): ").lower()

            # Get amount needed
            needed = num_check(f"Amount needed ({unit}): ", "float")

            while True:

                # Get amount bought
                bought = num_check(f"Amount bought ({unit}): ", "float")

                # Check amount bought is large enough
                if bought >= needed:
                    break

                else:
                    print("Amount bought cannot be smaller than amount needed.\n")

        # solid ingredients
        else:

            # Ask user for solid unit
            unit = input("Unit (g / kg): ").lower()

            # Get amount needed
            needed = num_check(f"Amount needed ({unit}): ", "float")

            while True:

                # Get amount bought
                bought = num_check(f"Amount bought ({unit}): ", "float")

                # Check amount bought is large enough
                if bought >= needed:
                    break

                else:
                    print("Amount bought cannot be smaller than amount needed.\n")

        # Add ingredient data to lists
        all_names.append(name)
        all_types.append(ing_type)
        amount_bought_list.append(bought)
        amount_needed_list.append(needed)

    # Create dataframe from dictionary
    ingredient_frame = pandas.DataFrame(ingredient_dict)

    # Calculate number of servings possible
    ingredient_frame["Servings Possible"] = (
            ingredient_frame["Amount Bought"]
            / ingredient_frame["Amount Needed"]
    )

    # Convert dataframe into formatted table
    ingredient_string = tabulate(
        ingredient_frame,
        headers='keys',
        tablefmt='psql',
        showindex=False
    )

    # Return formatted table
    return ingredient_string


# Main routine goes here

# Print title
print(make_statement("Recipe Ingredient Calculator", "🥘"))

# Get ingredient data
ingredients = get_ingredients()

# Print summary heading
print(make_statement("Ingredient Summary", "="))

# Display ingredient table
print(ingredients)