# Functions go here
def make_statement(statement, decoration):
    """Emphasises heading by adding decoration
    at the start and end"""

    print(f"{decoration * 3} {statement} {decoration * 3}")



def string_check(question, valid_ans_list=('yes', 'no'),
                 num_letters=1):
    """Checks that users enter the full word
    or the 'n' letter/s of a word from a list of valid responses"""

    while True:

        response = input(question).lower()

        for item in valid_ans_list:

            # check if the response is the entire word
            if response == item:
                return item

            # check if it's the 'n' letters
            elif response == item[:num_letters]:
                return item

        print(f"Please choose an option from valid {valid_ans_list}")


def Instructions():
    make_statement(statement="Instructions", decoration="🎉")

    print('''

DISPLAYS INSTRUCTIONS
    
    ''')


# Main routine goes here

make_statement(statement="Recipe Cost Calculator", decoration="🎉")

print()
want_instructions = string_check("Do you want to see the instructions? ")

if want_instructions == "yes":
    Instructions()

print()
print("Program continues...")