# import dependencies
import pandas as pd
import tabulate


"""
Need at least three functions beyond main that can be pytest-ed
must be named project.py, with test_project.py to test functions
requirements.txt

pytest - currency conversion, thirty percent buffer, final total, but maybe come up with something better, hmmmmm......

Start with a template, add editing extant csv, add blank creation, maybe bells and whistles?

Values to be wary of: Housing, Food, Total, Grand Total, 30% Buffer

Whiteboard:
create command line interface that creates or edits a csv
add a template csv, do not allow it to be saved over
split between new and old
ways to add and edit lines (expense, amount, notes), delete a line (add undo function?)
beware of commas in strings
function to convert currency to floats
function to calculate food expenses (boiler plate assumptions, plus special dinners, can be split by breakfast / lunch / dinner / snacks)
function to calculate housing costs (include option for multiple places)
function to increase activities? nah, just add a line
function that updates 30% buffer
function that updates final budget (sum)
Add a title / final notes / summary / something
export final budget to csv

this is going to be harder than i thought
"""


def main():

    # Greet User
    # eventually add option to edit extant csv's, or go rogue and make one up from scratch
    df = pd.read_csv("./resources/template.csv")
    print(df)
    print("""
          Welcome to the travel budget planner.
          Using the template above as a guide, it will customize your budget.
          It moves from flight costs to accomodations, food, and activities...
          ...to shopping, additional transportation, and miscellaneous fees.
          """)

    # set initial counter for rows
    counter = 0

    # call function to edit row, ask if they would like to add more values, return counter, counter += returned value
    # print output
    print(df.iloc[counter])
    # ask user if they want to change the values
    # if yes, check to see if Housing or Food


# def edit_row(counter): - add options in here for


# def currency_convert():


# def housing():


# def food():


# # pass the df and sum
# def thirty_percent_buffer():


    # this will be for editing extant budgets later
    # try:
    #     df = pd.read_csv("./resources/Namibia.csv")
    # except FileNotFoundError:
    #     print("File not Found. Creating a new one.")
    #     df = pd.DataFrame()

    # print(df)


if __name__ == "__main__":
    main()
