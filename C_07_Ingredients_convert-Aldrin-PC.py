import pandas
from tabulate import tabulate


# Functions go here
def make_statement(statement, decoration):
    """Emphasizes heading by adding decoration"""

    return f"\n{decoration * 3} {statement} {decoration * 3}\n"


def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again.\n")


def num_check(question, num_type="float"):
    """Checks that response is a float / integer more than zero"""

    # Checks if the number is more than zero
    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:
        try:

            if num_type == "float":
                response = float(input(question))
            else:
                response = int(input(question))

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)


def convert_liquid(amount, unit):
    """Convert liquid amounts to millilitres"""

    if unit == "l":
        return amount * 1000

    return amount


def convert_solid(amount, unit):
    """Convert solid amounts to grams"""

    if unit == "kg":
        return amount * 1000

    return amount


def get_ingredients():
    """Gets ingredient data with validation"""

    # Lists for dataframe
    all_names = []
    all_types = []
    amount_bought_list = []
    amount_needed_list = []

    # Ingredient dictionary
    ingredient_dict = {
        "Ingredient": all_names,
        "Type": all_types,
        "Amount Bought": amount_bought_list,
        "Amount Needed": amount_needed_list
    }

    # Ingredient loop
    while True:

        # Get ingredient name
        name = not_blank("Ingredient name (or 'xxx' to stop): ")

        # Check user enters at least one ingredient
        if name == "xxx" and len(all_names) == 0:
            print("You must enter at least one ingredient.\n")
            continue

        # End loop
        elif name == "xxx":
            break

        # Choose ingredient type (allows user to decide from whole,
        # liquid and solid ingredients)
        while True:
            ingred_type = input("Type whole (w) / liquid (l) / solid (s): ").lower()

            if ingred_type in ["whole", "w", "liquid", "l", "solid", "s"]:
                break

            print("Please choose 'whole', 'liquid', or 'solid'.\n")

        # whole ingredient
        if ingred_type in ["whole", "w"]:

            needed = num_check("How many needed? ", "integer")

            while True:
                bought = num_check("How many bought? ", "integer")

                # Prevent amount bought being smaller than amount needed
                if bought >= needed:
                    break

                print("Amount bought cannot be smaller than amount needed.\n")

        # liquid ingredient
        if ingred_type in ["liquid", "l"]:

            # Check valid liquid unit
            while True:
                unit = input("Unit (ml / L): ").lower()

                if unit in ["ml", "l"]:
                    break

                print("Please enter ml or L.\n")

            needed = num_check(f"Amount needed ({unit}): ", "float")

            while True:
                bought = num_check(f"Amount bought ({unit}): ", "float")

                if bought >= needed:
                    break

                print("Amount bought cannot be smaller than amount needed.\n")

            # Convert to ml
            bought = convert_liquid(bought, unit)
            needed = convert_liquid(needed, unit)

        # solid ingredient
        else:

            # Check valid solid unit
            while True:
                unit = input("Unit (g / kg): ").lower()

                if unit in ["g", "kg"]:
                    break

                print("Please enter g or kg.\n")

            needed = num_check(f"Amount needed ({unit}): ", "float")

            while True:
                bought = num_check(f"Amount bought ({unit}): ", "float")

                if bought >= needed:
                    break

                print("Amount bought cannot be smaller than amount needed.\n")

            # Convert to grams
            bought = convert_solid(bought, unit)
            needed = convert_solid(needed, unit)

        # Store data
        all_names.append(name)
        all_types.append(ingred_type)
        amount_bought_list.append(bought)
        amount_needed_list.append(needed)

    # Create dataframe
    ingredient_frame = pandas.DataFrame(ingredient_dict)

    # Calculate servings possible
    ingredient_frame["Servings Possible"] = (
            ingredient_frame["Amount Bought"]
            / ingredient_frame["Amount Needed"]
    )

    # Make dataframe into a table
    ingredient_string = tabulate(
        ingredient_frame,
        headers='keys',
        tablefmt='psql',
        showindex=False
    )

    return ingredient_string


# Main routine goes here

print(make_statement("Recipe Ingredient Calculator", "🥘"))

# Get ingredients
ingredients = get_ingredients()

# Output area
print(make_statement("Ingredient Summary", "="))
print(ingredients)