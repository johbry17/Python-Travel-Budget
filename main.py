# import dependencies
from dash import Dash, dcc, html, dash_table, callback, Input, Output, State
import pandas as pd

def main():
    app = Dash(__name__)

    # layout of html page
    app.layout = html.Div(
        [
            # header
            html.H1(
                "Travel Budget Planner",
                style={"textAlign": "center", "color": "blue", "fontSize": 30},
            ),
            # radio buttons to choose a budget
            html.Div(
                className="row",
                children=[
                    dcc.RadioItems(
                        options=[
                            "Tabula Rasa",
                            "Template Budget",
                            "Edinburgh",
                            "Machu Picchu",
                            "Namibia",
                            "Saint John Long Weekend",
                            "Saint John Weeklong",
                        ],
                        inline=True,
                        value="Template Budget",
                        id="radio-buttons",
                        style={"textAlign": "center"},
                    )
                ],
            ),
            # budget table
            dash_table.DataTable(id="budget-table"),
            html.Br(),
            # summary table
            dash_table.DataTable(id="summary-table", columns=[
                {"name": "Expense", "id": "Expense"},
                {"name": "Price", "id": "Price"},
                {"name": "Notes", "id": "Notes"},
            ]),
            # div for storing temporary data
            html.Div(id="hidden-div", style={"display": "none"}),
        ]
    )

    # decorator to update budget table
    @app.callback(
        Output("budget-table", "data"),
        Output("budget-table", "columns"),
        Input("radio-buttons", "value"),
    )
    def update_budget_table(button_chosen):
        # read in csv of selected budget
        budget = pd.read_csv(f"./resources/{button_chosen.replace(' ', '_')}.csv")
        # define columns, make them editable
        columns = [{"name": col, "id": col, "editable": True} for col in budget.columns]
        return [budget.to_dict("records"), columns]

    # decorator to update summary table
    @app.callback(
        Output("summary-table", "data"),
        Output("hidden-div", "children"),
        Input("budget-table", "data"),
    )
    def update_summary_table(current_data):
        if current_data:
            # convert current_data to dataframe
            df_temp = pd.DataFrame(current_data)

            # call functions to calculate total, 30% buffer, and grand total
            total = calc_total(df_temp)
            thirty_percent = calc_thirty_percent(total)
            grand_total = calc_grand_total(total, thirty_percent)

            # create summary table
            summary_data = pd.DataFrame({
                "Expense": ["Total", "30% Buffer", "Grand Total"],
                "Price": [total, thirty_percent, grand_total],
                "Notes": [
                    "Initial Estimate",
                    "Cause things are always WAY more expensive than you think",
                    "Sticker shock, eh? You CAN do this",
                ]
            }).to_dict("records")

            # update hidden_div with current_data
            hidden_div_content = df_temp.iloc[:-3, :].to_json(orient="split")

            return [summary_data, hidden_div_content]

        # return empty data if none exists
        return [[], None]

    if __name__ == "__main__":
        app.run(debug=True)


def calc_total(df):
    df.Price = pd.to_numeric(df.Price, errors='coerce')
    df.Price = df.Price.astype(float)
    return df.Price.sum()

def calc_thirty_percent(total):
    return 0.3 * total

def calc_grand_total(total, thirty_percent):
    return total + thirty_percent

if __name__ == "__main__":
    main()
