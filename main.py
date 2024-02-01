# import dependencies
from dash import Dash, dcc, html, dash_table, callback, Input, Output, State, ctx
import dash
from dash.dash_table import FormatTemplate
import pandas as pd
import dash_bootstrap_components as dbc


def main():
    app = Dash(
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    # layout of html page
    app.layout = html.Div(
        [
            # modal to confirm user wants to switch budgets
            dbc.Modal(
                [
                    dbc.ModalBody(
                        "Are you sure you want to continue? All work will be lost."
                    ),
                    dbc.ModalFooter(
                        html.Button(
                            "Proceed",
                            id="modal-proceed-button",
                            className="btn btn-primary",
                        )
                    ),
                ],
                id="confirmation-modal",
                centered=True,
            ),
            # hidden input to store the radio button selected
            dcc.Store(id="hidden-radio-store"),
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
                        # value="Template Budget", # uncomment to set default value
                        id="radio-buttons",
                        style={"textAlign": "center"},
                    )
                ],
            ),
            # budget table
            dash_table.DataTable(
                id="budget-table",
                editable=True,
                row_deletable=True,
                style_table={"overflowX": "auto"},  # enable horizontal scrolling
                style_cell={
                    "whiteSpace": "normal",
                    "height": "auto",
                },  # enable word wrap
            ),
            # buttons to add and delete rows
            html.Br(),
            html.Button("Add a Row", id="add-row-button", n_clicks=0),
            html.Button("Delete the Last Row", id="delete-row-button", n_clicks=0),
            html.Br(),
            # summary table
            dash_table.DataTable(
                id="summary-table",
                columns=[
                    {"name": "Expense", "id": "Expense"},
                    {
                        "name": "Price",
                        "id": "Price",
                        "type": "numeric",
                        "format": FormatTemplate.money(2),
                    },
                    {"name": "Notes", "id": "Notes"},
                ],
            ),
            # save button
            html.Button("Save and Download", id="save-button", n_clicks=0),
            # download link
            dcc.Download(id="download-link"),
        ]
    )

    # stores the selected radio button value
    # so that button_chosen is not None when the modal-proceed-button is clicked
    @app.callback(
        Output("hidden-radio-store", "data"),
        Input("radio-buttons", "value"),
    )
    def update_hidden_store(radio_value):
        return radio_value

    # update budget table
    @app.callback(
        # outputs budget table, budget table columns, and confirmation modal state
        Output("budget-table", "data"),
        Output("budget-table", "columns"),
        Output("confirmation-modal", "is_open"),
        # inputs any buttons clicked
        Input("modal-proceed-button", "n_clicks"),
        Input("add-row-button", "n_clicks"),
        Input("delete-row-button", "n_clicks"),
        Input("radio-buttons", "value"),
        Input("budget-table", "derived_virtual_data"),
        # states of the hidden selected radio button, budget table, and modal
        State("hidden-radio-store", "data"),
        State("budget-table", "data"),
        State("confirmation-modal", "is_open"),
        prevent_initial_call=True,
    )
    def update_budget_table(
        proceed,
        add_row,
        delete_row,
        radio_value,
        derived_virtual_data,
        button_chosen,
        # hidden_radio_store_data,
        current_data,
        is_modal_open,
    ):
        # get the button that was clicked, if any
        triggered_button = ctx.triggered_id
        # alternate, more verbose method that everyone seems to like better for explicitness
        # ctx = dash.callback_context
        # triggered_button = ctx.triggered[0]['prop_id'].split('.')[0]

        # when a radio button is selected, open the confirmation modal
        if triggered_button == "radio-buttons":
            return dash.no_update, dash.no_update, True

        # when the modal Proceed button is clicked, read in the csv of the selected budget
        elif (
            triggered_button == "modal-proceed-button"
            and button_chosen is not None
            and is_modal_open
        ):
            budget = pd.read_csv(f"./resources/{button_chosen.replace(' ', '_')}.csv")
            # return budget data and columns, and close the modal
            return (
                budget.to_dict("records"),
                [{"name": i, "id": i} for i in budget.columns],
                False,
            )

        # else convert the current_data to a DataFrame, with options to add or delete rows
        else:
            budget = pd.DataFrame(current_data)

            # adds a new row to the budget
            if "add-row-button" in triggered_button:
                new_row = {"Expense": "", "Price": "$0.00", "Notes": ""}
                budget = pd.concat([budget, pd.DataFrame([new_row])], ignore_index=True)
            # deletes the last row from the budget, unless it's the only row
            if "delete-row-button" in triggered_button and len(current_data) > 1:
                budget = budget.iloc[:-1]

            # reformat Price column, in case of user chicanery in the budget table
            if budget is not None and 'Price' in budget.columns:
                budget.Price = pd.to_numeric(
                    budget.Price.replace(r"[^\d.]", "", regex=True), errors="coerce"
                )
                budget.Price = budget.Price.astype(float).map("${:,.2f}".format)

            # return the budget data and columns, and do not change the modal
            return (
                budget.to_dict("records"),
                [{"name": i, "id": i} for i in budget.columns],
                dash.no_update,
            )

    # updates summary table, triggered by changes in the budget table
    @app.callback(
        Output("summary-table", "data"),
        Input("budget-table", "data"),
        prevent_initial_call=True,
    )
    def update_summary_table(data):
        # convert current_data to dataframe
        df = pd.DataFrame(data)

        # for initial load, do nothing
        # if 'Price' column does not exist, return the empty df
        if 'Price' not in df.columns:
            # return df.to_dict('records')
            return dash.no_update

        # strips all non-digit characters from the Price column, and converts to numeric - for maths!
        df.Price = pd.to_numeric(
            df.Price.replace(r"[^\d.]", "", regex=True), errors="coerce"
        )

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

        return summary_data

    # to download csv
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

            # reformat Price column, in case of user chicanery in the budget table
            df.Price = pd.to_numeric(
                df.Price.replace(r"[^\d.]", "", regex=True), errors="coerce"
            )
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
