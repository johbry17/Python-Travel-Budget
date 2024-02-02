# import dependencies
from dash import Dash, dcc, html, dash_table, callback, Input, Output, State, ctx
import dash
from dash.dash_table import FormatTemplate
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import re


def main():
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, "assets/style.css"])

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
                        [
                            html.Button(
                                "Proceed",
                                id="modal-proceed-button",
                                className="btn btn-primary",
                            ),
                            html.Button(
                                "Cancel",
                                id="modal-cancel-button",
                                className="btn btn-secondary",
                            ),
                        ]
                    ),
                ],
                id="confirmation-modal",
                centered=True,
            ),
            # header
            html.Div(
                children=[
                    html.H1("Travel Budget Planner", style={"color": "white"}),
                    html.P("Select a budget to get started", style={"color": "white", "font-size": "20px"}),
                    html.H6("**Bryan's ridiculous budget planner - now for the masses!", style={"color": "white", "font-size": "12px"}),
                ],
                style={
                "background-image": "url('/assets/background.jpg')",
                "background-size": "cover",
                "background-repeat": "no-repeat",
                "background-position": "center center",
                "text-align": "center",
                "color": "white",
                "padding": "50px",}
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
                        inputStyle={"margin-left": "10px"},
                        style={"textAlign": "center"},
                    )
                ],
            ),
            # hidden input to store the radio button selected
            dcc.Store(id="hidden-radio-store"),
            # budget table
            dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        dbc.Col(
                            dash_table.DataTable(
                                id="budget-table",
                                editable=True,
                                row_deletable=True, # cuidado!! danger!!
                                style_table={
                                    "overflowX": "auto"
                                },  # enable horizontal scrolling
                                style_cell={
                                    "whiteSpace": "normal",
                                    "height": "auto",# enable word wrap
                                    "border": "2px solid #888",
                                    "font-family": "Helvetica Neue, sans-serif",
                                },
                                style_data_conditional=[
                                    {"if": {"column_id": "Expense"}, "textAlign": "right"},
                                    {"if": {"column_id": "Price"}, "textAlign": "center"},
                                    {"if": {"column_id": "Notes"}, "textAlign": "left"},
                                    {
                                        "if": {"row_index": "odd"},
                                        "backgroundColor": "lightgrey"
                                    },
                                ],
                            ),
                            width=6,
                            className="mx-auto",
                        )
                    ),
                ),
                className="mb-3",
            ),
            # buttons to add and delete rows
            html.Div(
                className="d-flex justify-content-center",
                children=[
                    html.Button("Add a Row", id="add-row-button", n_clicks=0, style={"color": "green"}),
                    html.Button(
                        "Delete the Bottom Row", id="delete-row-button", n_clicks=0, style={"color": "red"}
                    ),
                ],
            ),
            html.Br(),
            html.Br(),
            # summary table
            dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        dbc.Col(
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
                                style_table={
                                    "overflowX": "auto"
                                },  # enable horizontal scrolling
                                style_cell={
                                    "whiteSpace": "normal",
                                    "height": "auto", # enable word wrap
                                    "border": "2px solid #888",
                                    "font-family": "Helvetica Neue, sans-serif",
                                },
                                style_data_conditional=[
                                    {"if": {"column_id": "Expense"}, "textAlign": "right"},
                                    {"if": {"column_id": "Price"}, "textAlign": "center"},
                                    {"if": {"column_id": "Notes"}, "textAlign": "left"},
                                    {
                                        "if": {"row_index": 1},
                                        "backgroundColor": "lightgrey"
                                    },
                                ],
                            ),
                            width=6,
                            className="mx-auto",
                        )
                    ),
                ),
                className="mb-3",
            ),
            # save button
            html.Div(
                className="d-flex justify-content-center",
                children=[
                    html.Button("Save and Download", id="save-button", n_clicks=0),
                ],
            ),
            # download link
            dcc.Download(id="download-link"),
            html.Br(),
            html.Br(),
            # donut chart of expenses
            dcc.Graph(id="expense-donut-chart"),
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
        Input("modal-cancel-button", "n_clicks"),
        Input("add-row-button", "n_clicks"),
        Input("delete-row-button", "n_clicks"),
        Input("radio-buttons", "value"),
        Input("budget-table", "derived_virtual_data"),  # realtime data changes to table
        # states of the hidden selected radio button, budget table, and modal
        State("hidden-radio-store", "data"),
        State("budget-table", "data"),
        State("confirmation-modal", "is_open"),
        prevent_initial_call=True,
    )
    def update_budget_table(
        proceed,
        cancel,
        add_row,
        delete_row,
        radio_value,
        derived_virtual_data,
        button_chosen,
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
            budget = pd.read_csv(f"./assets/{button_chosen.replace(' ', '_')}.csv")
            # return budget data and columns, and close the modal
            return (
                budget.to_dict("records"),
                [{"name": i, "id": i} for i in budget.columns],
                False,
            )

        # when the modal Cancel button is clicked, do nothing and close the modal
        elif triggered_button == "modal-cancel-button" and is_modal_open:
            return dash.no_update, dash.no_update, False

        # else convert the current_data to a DataFrame, with options to add or delete rows
        # & autoformat the Price column, using derived_virtual_data (realtime data changes to table)
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
            if budget is not None and "Price" in budget.columns:
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
        if "Price" not in df.columns:
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

            # convert combined dataframe to csv file
            csv_file = df.to_csv(index=False, encoding="utf-8")

            # create download link
            download_link = dict(
                content=csv_file, filename="travel_budget.csv", type="text/csv"
            )

            return download_link
        
    # callback to update donut chart
    @app.callback(
        Output("expense-donut-chart", "figure"),
        Input("budget-table", "data"),
        Input("summary-table", "data"),
        prevent_initial_call=True,
    )
    def update_donut_chart(budget_data, summary_data):
        # if budget_data is empty (initial load), return an empty figure
        if not budget_data:
            return go.Figure()

        # extract labels and values from the budget data
        labels = [row["Expense"] for row in budget_data]
        values = [row["Price"] for row in budget_data]

        # strip all non-digit chars from values, and convert to float
        values = [float(re.sub(r"[^\d.]", "", value)) for value in values]

        # Add the buffer from the summary data
        labels.append("Now 23.1% Buffer")
        buffer_value = next((row["Price"] for row in summary_data if row["Expense"] == "30% Buffer"), 0)
        values.append(buffer_value)

        # Calculate the total amount
        total = sum(values)

        # Calculate the percentages
        percentages = [value / total for value in values] if total != 0 else values

        title=f"Breakdown of Expenses<br>${total:.2f} Total"

        # Create the figure
        figure = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=percentages,
                    text=values,
                    hole=.5,
                    hovertemplate="%{label}:  $%{text:.2f}<extra></extra>",
                    textinfo="percent",
                )
            ],
            layout=go.Layout(
                title="Breakdown of Expenses",
                showlegend=True,
                annotations=[
                    dict(
                        x=0.5,
                        y=-0.1,
                        showarrow=False,
                        text=f"Total: ${total:.2f}",
                        xref="paper",
                        yref="paper",
                        font=dict(
                            size=20,
                        )
                    )
                ]
            ),
        )

        return figure

    # initialize the app
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
