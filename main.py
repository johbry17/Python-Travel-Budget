# import dependencies
from dash import Dash, dcc, html, dash_table, callback, Input, Output, State, ctx
import dash
from dash.dash_table import FormatTemplate
import pandas as pd
import dash_bootstrap_components as dbc


def main():
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],)

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
                        value="Template Budget", # uncomment to set default value
                        id="radio-buttons",
                        style={"textAlign": "center"},
                    )
                ],
            ),
            # budget table
            dash_table.DataTable(
                id="budget-table",
                # columns=[
                #     {"name": "Expense", "id": "Expense", "editable": True},
                #     {"name": "Price", "id": "Price", "editable": True, "type": "numeric", "format": FormatTemplate.money(2)},
                #     {"name": "Notes", "id": "Notes", "editable": True},
                #     # Add a column for buttons
                #     {"name": "Actions", "id": "button-column", "editable": False, "hideable": True},
                # ],
                editable=True,
                row_deletable=True,
                # style_table={"overflowX": "auto"},
            ),
            html.Br(),
            html.Button("Add Row", id="add-row-button", n_clicks=0),
            html.Button("Delete Row", id="delete-row-button", n_clicks=0),
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
            # save button
            html.Button("Save and Download", id="save-button", n_clicks=0),
            # download link
            dcc.Download(id="download-link"),
            # hidden div for storing temporary data
            html.Div(id="hidden-div", style={"display": "none"}),
        ]
    )

    # update budget table
    @app.callback(
        Output("budget-table", "data"),
        Output("budget-table", "columns"),
        Input("radio-buttons", "value"),
        Input("add-row-button", "n_clicks"),
        Input("delete-row-button", "n_clicks"),
        State("budget-table", "data"),
        # prevent_initial_call=True,
    )
    def update_budget_table(button_chosen, add_row, delete_row, current_data):
        # check if button was chosen
        if button_chosen and button_chosen != "Template Budget" or not current_data:
            # read in csv of selected budget
            budget = pd.read_csv(f"./resources/{button_chosen.replace(' ', '_')}.csv")
            columns = [{"name": col, "id": col, "editable": True} for col in budget.columns]
        else:
            budget = pd.DataFrame(current_data)
            columns = [{"name": col, "id": col, "editable": True} for col in budget.columns]

        # define columns, make them editable
        # columns = [{"name": col, "id": col, "editable": True} for col in budget.columns]

        # strip dollar sign (if extant) from Price column
        budget.Price = pd.to_numeric(budget.Price.replace("[\$,]", "", regex=True), errors="coerce")

        # format Price column as currency
        budget.Price = budget.Price.astype(float).map("${:,.2f}".format)

        # check which button was clicked
        # ctx = dash.callback_context
        triggered_button = ctx.triggered_id

        # print("triggered_button Test:")
        # print(triggered_button)

        if triggered_button:
            if "add-row-button" in triggered_button:
                # new_row = pd.DataFrame({"Expense": [""], "Price": [0], "Notes": [""]})
                new_row = {"Expense": "", "Price": 0, "Notes": ""}
                budget = pd.concat([budget, pd.DataFrame([new_row])], ignore_index=True)
            if "delete-row-button" in triggered_button and len(current_data) > 0:
                budget = budget.iloc[:-1]

        return [budget.to_dict("records"), columns]
        # return [current_data, columns]

    # update summary table
    @app.callback(
        Output("summary-table", "data"),
        Output("hidden-div", "children"),
        Input("budget-table", "data"),
        # prevent_initial_call=True,
    )
    def update_summary_table(data):
        # convert current_data to dataframe
        df = pd.DataFrame(data)

        # strip any none digit input (if extant) from the Price column
        df.Price = pd.to_numeric(df.Price.replace("[^\d.]", "", regex=True), errors="coerce")

        # call functions to calculate total, 30% buffer, and grand total
        total = calc_total(df)
        thirty_percent = calc_thirty_percent(total)
        grand_total = calc_grand_total(total, thirty_percent)

        # create summary table
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

        # format Price column as currency
        df.Price = df.Price.map("${:,.2f}".format)

        # update hidden_div with current_data
        hidden_div_content = df.to_json(orient="split")

        return [summary_data, hidden_div_content]
        # return [summary_data]

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

            # reformat Price column, as I can't get the budget-table to update
            df.Price = pd.to_numeric(df.Price.replace("[\$,]", "", regex=True), errors="coerce")
            df.Price = df.Price.astype(float).map("${:,.2f}".format)

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
