# import dependencies
import pandas as pd


"""
Need at least three functions beyond main that can be pytest-ed
main.py must be renamed project.py, with test_project.py to test functions
requirements.txt

Whiteboard:
create command line interface that creates or edits a csv
add a template csv, do not allow it to be saved over
ways to add and edit lines (expense, amount, notes)
function to calculate dinner expenses (boiler plate assumptions, plus special dinners)
function to calculate housing costs (include option for multiple places)
function to increase activities? nah, just add a line
function that updates 30% buffer
function that updates final budget (sum)
export final budget to csv
"""


def main():
    try:
        df = pd.read_csv("test_Machu_Picchu.csv")
    except FileNotFoundError:
        print("File not Found. Creating a new one.")
        df = pd.DataFrame()
    
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()