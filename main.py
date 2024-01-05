# import dependencies
import pandas as pd
from tabulate import tabulate
import sys


"""
Need at least three functions beyond main that can be pytest-ed
must be named project.py, with test_project.py to test functions
requirements.txt

pytest - currency conversion, thirty percent buffer, final total, but maybe come up with something better, hmmmmm......

Start with a template, add editing extant csv, add blank creation, maybe bells and whistles?

Values to be wary of: Housing, Food, Total, Grand Total, 30% Buffer

add a template csv, do not allow it to be saved over
split between new and old
ways to add and edit lines (expense, amount, notes), delete a line (add undo function?)
beware of commas in strings
function to increase activities? nah, just add a line
Add a title / final notes / summary / something
remember to fix numbering in main for user choices

this is going to be harder than i thought
"""


def main():
    # Greet User
    print(
        """
          Welcome to the travel budget planner.
          It will guide you through creating a budget for your dream vacation."""
    )

    # map options to functions
    options = {
        "0": example_budgets,
        "1": initialize_budget,
        # '3': add_row,
        # '4': edit_row,
        "5": save_and_exit,
    }

    # initialize dataframe to hold budget
    df = pd.DataFrame()

    # print options for user
    # this is a recursize loop, and only terminates if the user chooses to save and / or exit
    while True:
        print("\nWould you like to:")
        print("0) See examples and get a tutorial   1) Start or load a budget   3) Add a row   4) Edit a row   5) Save and / or exit""")
        user_input = input("What would you like to do?")

        # call function based on user input
        choice = options.get(user_input)
        if choice:
            choice(df)
        else:
            print("Invalid choice")


# def display_budget(budget):


def example_budgets(df):
    # map user choices to budget names
    budgets = {
        "0": "template",
        "1": "Edinburgh",
        "2": "Machu_Picchu",
        "3": "Namibia",
        "4": "Saint_John_Long_Weekend",
        "5": "Saint_John_Weeklong",
    }

    # print options for user and solicit input
    print("\nExample budgets:")
    for key, value in budgets.items():
        print(f"{key}) {value.replace('_', ' ')}")
    user_input = input("What would you like to do?")

    budget = budgets.get(user_input)
    if budget:
        example_df = pd.read_csv(f"./resources/{budget}.csv")
        print(tabulate(example_df, headers="keys", tablefmt="grid"))
        print("\nTutorial: Fill in 'Expense', 'Price', and 'Notes' when creating your custom budget")
        print("The budget planner automatically adds a 30% buffer and totals projected expenses")
    else:
        print("Invalid choice")

    # return True


def initialize_budget(df):
    # ask for user input
    user_input = input("Do you wish to: \n0) Load an extant budget, \n1) Use a template budget, \n2) Create a blank budget?")

    if user_input == '0':
        name = input("What is the name of the budget? Precision is necessary.")
        df = pd.read_csv(f"./saved/{name}.csv")


# def edit_row(counter): - add options in here for deletion as well


def save_and_exit(df):
    sys.exit()


# convert currency to floats
# def currency_convert():


# calculate housing costs (include option for multiple places)
# def housing():


# calculate food expenses (boiler plate assumptions, plus special dinners, can be split by breakfast / lunch / dinner / snacks)
# def food():


# # pass the df and sum
# def calculate_thirty_percent_buffer():

# this will be for editing extant budgets later
# try:
#     df = pd.read_csv("./resources/Namibia.csv")
# except FileNotFoundError:
#     print("File not Found. Creating a new one.")
#     df = pd.DataFrame()

# print(df)

# function that updates final budget (sum)
# def calculate_sum():


if __name__ == "__main__":
    main()
