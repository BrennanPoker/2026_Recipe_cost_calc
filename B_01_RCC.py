import pandas
from tabulate import tabulate


# Functions go here
def make_statement(statement, decoration):
    """Emphasises heading"""
    print(f"\n{decoration * 3} {statement} {decoration * 3}\n")


def string_check(question, valid_ans_list=("yes", "no"), num_letters=1):
    """Checks yes/no responses"""

    while True:
        response = input(question).lower()

        for item in valid_ans_list:
            if response == item:
                return item
            elif response == item[:num_letters]:
                return item

        print(f"Please choose from {valid_ans_list}.")


def instructions():
    make_statement("Instructions", "📖")

    print("""
Welcome to the Recipe Cost Calculator.

You will be asked to:
- Enter the recipe name.
- Enter the number of servings.
- Enter each ingredient.
- Enter how much you bought and how much is used.
- Enter the cost of the ingredient.

The program will calculate:
- Cost of each ingredient used.
- Total recipe cost.
- Cost per serving.
""")


def not_blank(question):
    """Checks input isn't blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank.\n")


def num_check(question, num_type="float"):
    """Checks numbers are greater than zero"""

    if num_type == "float":
        error = "Please enter a number greater than 0."
    else:
        error = "Please enter an integer greater than 0."

    while True:
        try:

            if num_type == "float":
                response = float(input(question))
            else:
                response = int(input(question))

            if response > 0:
                return response

            print(error)

        except ValueError:
            print(error)


def ingredient_cost_used(cost, amount_bought, amount_needed):
    """Calculates ingredient cost used"""

    return round((amount_needed / amount_bought) * cost, 2)


def convert_amount(amount, unit):
    """Converts litres/kg into ml/g"""

    conversions = {
        "l": ("ml", 1000),
        "kg": ("g", 1000),
        "ml": ("ml", 1),
        "g": ("g", 1)
    }

    new_unit, multiplier = conversions[unit]
    return amount * multiplier, new_unit


def get_ingredients():
    """Gets ingredient information"""

    # Lists for dataframe
    all_names = []
    all_types = []
    amount_bought_list = []
    amount_needed_list = []
    cost_list = []
    cost_used_list = []

    total_recipe_cost = 0

    # Ingredient dictionary
    ingredient_dict = {
        "Ingredient": all_names,
        "Type": all_types,
        "Amount Bought": amount_bought_list,
        "Amount Needed": amount_needed_list,
        "Cost ($)": cost_list,
        "Cost Used ($)": cost_used_list
    }

    # Ingredient loop
    while True:

        # Get ingredient name
        name = not_blank("\nIngredient name (or 'xxx' to stop): ")

        # Check user enters at least one ingredient
        if name == "xxx":

            if len(all_names) == 0:
                print("Please enter at least one ingredient.")
                continue

            # Ends loop
            break

        # Choose ingredient type
        while True:

            ingred_type = input("Type (whole / liquid / solid): ").lower()

            if ingred_type in ["whole", "w", "liquid", "l", "solid", "s"]:
                break

            print("Please enter whole, liquid or solid.")

        # Convert shortcuts into full words
        if ingred_type in ["whole", "w"]:
            ingred_type = "whole"

        elif ingred_type in ["liquid", "l"]:
            ingred_type = "liquid"

        else:
            ingred_type = "solid"

        # whole ingredients
        if ingred_type == "whole":

            unit = "item(s)"

            needed = num_check("How many needed? ", "integer")

            while True:

                bought = num_check("How many bought? ", "integer")

                if bought >= needed:
                    break

                print("Amount bought cannot be less than amount needed.")

        # liquid / solid ingredients
        else:

            if ingred_type == "liquid":
                valid_units = ["ml", "l"]
                unit_text = "ml/L"

            else:
                valid_units = ["g", "kg"]
                unit_text = "g/kg"

            # gets unit type for conversion and final table
            while True:

                unit = input(f"Unit ({unit_text}): ").lower()

                if unit in valid_units:
                    break

                print("Invalid unit.")

            needed = num_check(f"Amount needed ({unit}): ")

            while True:

                bought = num_check(f"Amount bought ({unit}): ")

                # makes sure that amount bought is higher than amount needed
                # (you can't make something without the right amount of ingredient)
                if bought >= needed:
                    break

                print("Amount bought cannot be less than amount needed.")

            bought, unit = convert_amount(bought, unit)
            needed, unit = convert_amount(needed, unit)

        cost = num_check(f"Cost of {bought} {unit} ($): ")

        used_cost = ingredient_cost_used(cost, bought, needed)

        total_recipe_cost += used_cost

        # Store data
        all_names.append(name)
        all_types.append(ingred_type)

        amount_bought_list.append(f"{bought} {unit}")
        amount_needed_list.append(f"{needed} {unit}")

        cost_list.append(f"${cost:.2f}")
        cost_used_list.append(f"${used_cost:.2f}")

    # Create dataframe
    ingredient_frame = pandas.DataFrame(ingredient_dict)

    # Make dataframe into a table
    ingredient_table = tabulate(
        ingredient_frame,
        headers="keys",
        tablefmt="psql",
        showindex=False
    )

    return ingredient_table, total_recipe_cost


# Main Routine

make_statement("Recipe Cost Calculator", "🥘")

want_instructions = string_check("Do you want to see the instructions? ")

if want_instructions == "yes":
    instructions()

print()

# Gets recipe name and serving size and outputs
recipe_name = not_blank("Recipe name: ")
serving_size = num_check("Serving size: ", "integer")

print(f"\nYou are making {serving_size} servings of {recipe_name}.")


ingredient_table, total_recipe_cost = get_ingredients()

# Gets cost per serving size
cost_per_serving = total_recipe_cost / serving_size

# Output area
make_statement("Recipe Summary", "=")

print(f"Recipe: {recipe_name}")
print(f"Servings: {serving_size}\n")

print(ingredient_table)

print(f"\nTotal Recipe Cost: ${total_recipe_cost:.2f}")
print(f"Cost Per Serving: ${cost_per_serving:.2f}")