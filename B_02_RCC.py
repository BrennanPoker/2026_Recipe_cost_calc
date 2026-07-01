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
    """Converts L / kg into ml / g"""

    conversions = {
        "l": ("ml", 1000),
        "kg": ("g", 1000),
        "ml": ("ml", 1),
        "g": ("g", 1)
    }

    new_unit, multiplier = conversions[unit]
    return amount * multiplier, new_unit

def display_amount(amount, unit):
    """Converts g to kg and ml to L for final table"""

    if unit == "g":
        if amount >= 1000:
            return f"{amount / 1000:g} kg"
        return f"{amount:g} g"

    elif unit == "ml":
        if amount >= 1000:
            return f"{amount / 1000:g} L"
        return f"{amount:g} ml"
    return f"{amount:g} {unit}"

def get_ingredients():
    """Collects ingredient information and creates a table."""

    # Lists for dataframe
    names, types = [], []
    bought_list, needed_list = [], []
    cost_list, used_cost_list = [], []

    total_recipe_cost = 0

    ingredient_type_map = {
        "w": "whole", "whole": "whole",
        "l": "liquid", "liquid": "liquid",
        "s": "solid", "solid": "solid"
    }

    unit_options = {
        "liquid": (["ml", "l"], "ml / L"),
        "solid": (["g", "kg"], "g / kg")
    }

    while True:

        name = not_blank("\nIngredient name (or 'xxx' to stop): ")

        if name == "xxx":
            if len(names) == 0:
                print("Please enter at least one ingredient.")
                continue
            break

        # Ingredient type selection
        while True:
            ingred_type = input("Type (whole / liquid / solid): ").lower()

            if ingred_type in ingredient_type_map:
                ingred_type = ingredient_type_map[ingred_type]
                break

            print("Please enter whole, liquid or solid.")

        # Whole ingredients
        if ingred_type == "whole":

            unit = "item(s)"

            needed = num_check("How many needed? ", "integer")
            bought = num_check("How many bought? ", "integer")


        # Liquid / solid ingredients
        else:
            valid_units, unit_text = unit_options[ingred_type]

            while True:
                unit = input(f"Unit ({unit_text}): ").lower()
                if unit in valid_units:
                    break
                print("Invalid unit.")

            needed = num_check(f"Amount needed ({unit}): ")
            bought = num_check(f"Amount bought ({unit}): ")

            # Converts both amounts
            bought, converted_unit = convert_amount(bought, unit)
            needed, _ = convert_amount(needed, unit)

            unit = converted_unit

        cost = num_check(f"Cost of {bought} {unit} ($): ")

        used_cost = ingredient_cost_used(cost, bought, needed)
        total_recipe_cost += used_cost

        # Store values for table
        names.append(name)
        types.append(ingred_type)

        bought_list.append(display_amount(bought, unit))
        needed_list.append(display_amount(needed, unit))

        cost_list.append(f"${cost:.2f}")
        used_cost_list.append(f"${used_cost:.2f}")

    # Ingredient dictionary
    ingredient_dict = {
        "Ingredient": names,
        "Type": types,
        "Amount Bought": bought_list,
        "Amount Needed": needed_list,
        "Cost ($)": cost_list,
        "Cost Used ($)": used_cost_list
    }

    # Creates dataframe
    dataframe = pandas.DataFrame(ingredient_dict)

    # Makes dataframe into a table
    table = tabulate(dataframe,
                     headers="keys",
                     tablefmt="psql",
                     showindex=False)

    return table, total_recipe_cost


# Main Routine

# Program title (so they know what they're using
make_statement("Recipe Cost Calculator", "🥘")

# Asks if user wants instructions
want_instructions = string_check("Do you want to see the instructions? ")

# if they want it'll print instructions
if want_instructions == "yes":
    instructions()

print()

# Gets recipe name and serving size and outputs
recipe_name = not_blank("Recipe name: ")
serving_size = num_check("Serving size: ", "integer")

# Tells the user what they just inputted to ensure it looks correct
print(f"\nYou are making {serving_size} servings of {recipe_name}.")


ingredient_table, total_recipe_cost = get_ingredients()

# Gets cost per serving size
cost_per_serving = total_recipe_cost / serving_size

# Output area... Recipe summary area
# (Restates Recipe and serving size, as well as shows table
# and final cost and cost per serving)
make_statement("Recipe Summary", "=")

print(f"Recipe: {recipe_name}")
print(f"Servings: {serving_size}\n")

print(ingredient_table)

print(f"\nTotal Recipe Cost: ${total_recipe_cost:.2f}")
print(f"Cost Per Serving: ${cost_per_serving:.2f}")