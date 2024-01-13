# import dependencies
from dash import Dash, dcc, html, dash_table, callback, Input, Output
import pandas as pd

"""
Need at least three functions beyond main that can be pytest-ed
must be named project.py, with test_project.py to test functions
requirements.txt

pytest - currency conversion, thirty percent buffer, final total, but maybe come up with something better, hmmmmm......
"""


def main():
    app = Dash(__name__)

    # initialize empty df
    df = pd.DataFrame()

    # main layout of html page
    app.layout = html.Div([
        # header
        html.H1("Travel Budget Planner", style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

        # radio buttons to choose a budget
        html.Div(className='row', children=[
            dcc.RadioItems(options=['Tabula Rasa', 'Template Budget', 'Edinburgh', 'Machu Picchu', 'Namibia', 'Saint John Long Weekend', 'Saint John Weeklong'], inline=True, value='Template Budget', id='radio-buttons', style={'textAlign': 'center'})
        ]),

        # div to contain budget table
        html.Div(id='budget'),
    ])

    # decorator for function to update table
    @app.callback(
        # specify output and input by html id
        Output('budget', 'children'),
        Input('radio-buttons', 'value')
    )
    # actual function that loads chosen budget into a dash DataTable
    def update_table(button_chosen):
        if button_chosen:
            budget = pd.read_csv(f"./resources/{button_chosen.replace(' ', '_')}.csv")
            return dash_table.DataTable(
                data=budget.to_dict('records'),
            )


    if __name__ == "__main__":
        app.run(debug=True)


if __name__ == "__main__":
    main()
