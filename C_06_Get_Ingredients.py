import pandas

def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again.\n")


def num_check(question, num_type="float"):
    """Checks that response is a float / integer more than zero"""

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


def get_ingredients():
    """Gets ingredient data with type-specific validation"""

    all_names = []
    all_types = []
    amount_bought_list = []
    amount_needed_list = []

    ingredient_dict = {
        "Ingredient": all_names,
        "Type": all_types,
        "Amount Bought": amount_bought_list,
        "Amount Needed": amount_needed_list
    }

    while True:
        name = not_blank("Ingredient name (or 'xxx' to stop): ")

        if name == "xxx":
            if len(all_names) == 0:
                print("You must enter at least one ingredient.\n")
                continue
            break

        while True:
            ing_type = input("Type (whole / liquid / solid): ").lower()

            if ing_type in ["whole", "liquid", "solid"]:
                break
            else:
                print("Please choose 'whole', 'liquid', or 'solid'.")

        if ing_type == "whole":
            bought = num_check("How many bought? ", "integer")
            needed = num_check("How many needed? ", "integer")

        elif ing_type == "liquid":
            unit = input("Unit (ml / L): ").lower()
            bought = num_check(f"Amount bought ({unit}): ", "float")
            needed = num_check(f"Amount needed ({unit}): ", "float")

        else:
            unit = input("Unit (g / kg): ").lower()
            bought = num_check(f"Amount bought ({unit}): ", "float")
            needed = num_check(f"Amount needed ({unit}): ", "float")

        all_names.append(name)
        all_types.append(ing_type)
        amount_bought_list.append(bought)
        amount_needed_list.append(needed)

    ingredient_frame = pandas.DataFrame(ingredient_dict)

    return ingredient_frame


# Main routine goes here

# testing function
def main():
    ingredients = get_ingredients()

    print("\n--- Ingredient Summary ---")
    print(ingredients)


# run the program
if __name__ == "__main__":
    main()
