# import dependencies
from dash import Dash, dcc, html, dash_table, callback, Input, Output, State
from dash.dash_table import FormatTemplate
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
            dash_table.DataTable(
                id="summary-table",
                columns=[
                    {"name": "Expense", "id": "Expense"},
                    {"name": "Price", "id": "Price", "type": "numeric", "format": FormatTemplate.money(2)},
                    {"name": "Notes", "id": "Notes"},
                ],
            ),
            # div for storing temporary data
            html.Div(id="hidden-div", style={"display": "none"}),
            # save button
            html.Button("Save and Download", id="save-button", n_clicks=0),
            # download link
            dcc.Download(id="download-link"),
        ]
    )


    # update tables
    @app.callback(
        [
            Output("budget-table", "data"),
            Output("budget-table", "columns"),
            Output("summary-table", "data"),
            Output("hidden-div", "children"),
        ],
        [
            Input("radio-buttons", "value"),
            Input("hidden-div", "children"),
        ],
        prevent_initial_call=True  # This prevents the callback from running on app initialization
    )
    def update_tables(button_chosen, hidden_div_content):
        # read in csv of selected budget
        budget = pd.read_csv(f"./resources/{button_chosen.replace(' ', '_')}.csv")
        
        # define columns for budget table
        columns_budget = [{"name": col, "id": col, "editable": True} for col in budget.columns]

        if hidden_div_content:
            temp_data = pd.read_json(hidden_div_content, orient="split")
            temp_data['Price'] = pd.to_numeric(temp_data['Price'].replace('[\$,]', '', regex=True), errors='coerce')

            budget.update(temp_data)

        # strip dollar sign from Price column
        budget['Price'] = pd.to_numeric(budget['Price'].replace('[\$,]', '', regex=True), errors='coerce')

        # format Price column with dollar sign
        # budget['Price'] = budget['Price'].astype(float).map("${:,.2f}".format)

        # calculate summary data
        total = calc_total(budget)
        thirty_percent = calc_thirty_percent(total)
        grand_total = calc_grand_total(total, thirty_percent)

        # create summary table data
        summary_data = pd.DataFrame(
            {
                "Expense": ["Total", "30% Buffer", "Grand Total"],
                "Price": [total, thirty_percent, grand_total],
                "Notes": [
                    "Initial Estimate",
                    "Cause things are always WAY more expensive than you think",
                    "Sticker shock, eh? You CAN do this",
                ],
            }
        ).to_dict("records")

        # update hidden_div with current_data
        hidden_div_content = budget.to_json(orient="split")

        # format Price column with dollar sign
        budget['Price'] = budget['Price'].astype(float).map("${:,.2f}".format)

        return [budget.to_dict("records"), columns_budget, summary_data, hidden_div_content]

    # download csv
    @app.callback(
        Output("download-link", "data"),
        Input("save-button", "n_clicks"),
        State("budget-table", "data"),
        State("summary-table", "data"),
    )
    def save_data(n_clicks, budget_data, summary_data):
        if n_clicks > 0:
            # convert budget_data and summary_data to dataframes
            budget_df = pd.DataFrame(budget_data)
            summary_df = pd.DataFrame(summary_data)

            # append summary_df to budget_df
            df = pd.concat([budget_df, summary_df], ignore_index=True)

            # convert combined dataframe to csv file
            csv_file = df.to_csv(index=False, encoding="utf-8")

            # create download link
            download_link = dict(
                content=csv_file, filename="travel_budget.csv", type="text/csv"
            )

            return download_link

    if __name__ == "__main__":
        app.run(debug=True)


# function to calculate total
def calc_total(df):
    df.Price = pd.to_numeric(df.Price, errors="coerce")
    df.Price = df.Price.astype(float)
    return df.Price.sum()


# function to calculate 30% buffer
def calc_thirty_percent(total):
    return 0.3 * total


# function to calculate grand total
def calc_grand_total(total, thirty_percent):
    return total + thirty_percent


if __name__ == "__main__":
    main()
