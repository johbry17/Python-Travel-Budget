# import dependencies
import dash
from dash import Dash, dcc, html, dash_table, callback, Input, Output, State, ctx
from dash.dash_table import FormatTemplate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import re


def main():
    """
    Main function to run the app.
    First, it initializes the app, then it sets up the layout of the html page.
    Next, it sets up the callbacks to update the budget table, summary table, and donut chart.
    Finally, it initializes the app.
    """
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    """
    Initializes the app with the name of the module, and the external stylesheets to use.
    Layout immediately below.
    """

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
                    html.P(
                        "Select a budget to get started",
                        style={"color": "white", "font-size": "20px"},
                    ),
                    html.H6(
                        "**Bryan's ridiculous budget planner - now for the masses!",
                        style={"color": "white", "font-size": "12px"},
                    ),
                ],
                style={
                    "background-image": "url('/assets/background.jpg')",
                    "background-size": "cover",
                    "background-repeat": "no-repeat",
                    "background-position": "center center",
                    "text-align": "center",
                    "color": "white",
                    "padding": "50px",
                },
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
                                row_deletable=True,  # cuidado!! danger!!
                                style_table={
                                    "overflowX": "auto"
                                },  # enable horizontal scrolling
                                style_cell={
                                    "whiteSpace": "normal",
                                    "height": "auto",  # enable word wrap
                                    "border": "2px solid #888",
                                    "font-family": "Helvetica Neue, sans-serif",
                                },
                                style_data_conditional=[
                                    {
                                        "if": {"column_id": "Expense"},
                                        "textAlign": "right",
                                    },
                                    {
                                        "if": {"column_id": "Price"},
                                        "textAlign": "center",
                                    },
                                    {"if": {"column_id": "Notes"}, "textAlign": "left"},
                                    {
                                        "if": {"row_index": "odd"},
                                        "backgroundColor": "lightgrey",
                                    },
                                ],
                            ),
                        )
                    ),
                ),
                className="mb-3",
            ),
            # buttons to add and delete rows
            html.Div(
                className="d-flex justify-content-center",
                children=[
                    html.Button(
                        "Add a Row",
                        id="add-row-button",
                        n_clicks=0,
                        style={"color": "green"},
                    ),
                    html.Button(
                        "Delete the Bottom Row",
                        id="delete-row-button",
                        n_clicks=0,
                        style={"color": "red"},
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
                                    "height": "auto",  # enable word wrap
                                    "border": "2px solid #888",
                                    "font-family": "Helvetica Neue, sans-serif",
                                },
                                style_data_conditional=[
                                    {
                                        "if": {"column_id": "Expense"},
                                        "textAlign": "right",
                                    },
                                    {
                                        "if": {"column_id": "Price"},
                                        "textAlign": "center",
                                    },
                                    {"if": {"column_id": "Notes"}, "textAlign": "left"},
                                    {
                                        "if": {
                                            "row_index": 1
                                        },  # yeah, I know, it's a hack
                                        "backgroundColor": "lightgrey",
                                    },
                                ],
                            ),
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
            # donut chart of expenses
            dcc.Graph(id="expense-donut-chart"),
        ]
    )

    # update hidden store with selected radio button value
    @app.callback(
        Output("hidden-radio-store", "data"),
        Input("radio-buttons", "value"),
    )
    def update_hidden_store(radio_value):
        """
        Update hidden store with selected radio button value...
        ...so that button_chosen is not None when the modal-proceed-button is clicked.
        """
        return radio_value

    # updates budget table
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
        """
        Update budget table, budget table columns, and confirmation modal state...
        ...based on the button clicked, the selected radio button, the current data, and the modal state.
        If the radio button is selected, open the confirmation modal.
        If the modal Proceed button is selected, read in the selected csv.
        If the modal Cancel button is selected, do nothing.
        The last conditional updates the budget in realtime, and autoformats the Price column.
        With options to add or delete rows.
        Return values in order are always budget data, budget columns, and modal state.
        """
        # get the button that was clicked, if any - ctx = dash.callback_context
        triggered_button = ctx.triggered_id

        # opens the confirmation modal
        if triggered_button == "radio-buttons":
            return dash.no_update, dash.no_update, True

        # closes the confirmation modal, and reads in the selected csv
        elif triggered_button == "modal-proceed-button" and is_modal_open:
            budget = pd.read_csv(f"./assets/csv/{button_chosen.replace(' ', '_')}.csv")
            return (
                budget.to_dict("records"),
                [{"name": i, "id": i} for i in budget.columns],
                False,
            )

        # does nothing but close the modal
        elif triggered_button == "modal-cancel-button" and is_modal_open:
            return dash.no_update, dash.no_update, False

        # for editing current table in realtime, with add/delete row buttons
        else:
            budget = pd.DataFrame(current_data)
            if "add-row-button" in triggered_button:
                budget = add_new_row(budget)
            if "delete-row-button" in triggered_button and len(current_data) > 1:
                budget = budget.iloc[:-1]
            return (
                format_price(budget).to_dict("records"),
                [{"name": i, "id": i} for i in budget.columns],
                dash.no_update,
            )

    # updates summary table
    @app.callback(
        Output("summary-table", "data"),
        Input("budget-table", "data"),
        prevent_initial_call=True,
    )
    def update_summary_table(data):
        """
        Updates summary table based on the budget table data, first formatting the Price column...
        ...the caling the subtotal, 30% buffer, and grand total functions.
        And then returns the summary data as a DataFrame.
        """
        df = pd.DataFrame(data)

        # for initial load, do nothing, or it throws an attribute error
        if "Price" not in df.columns:
            return dash.no_update

        # strips all non-digit characters from the Price column, and converts to numeric - for maths!
        df.Price = pd.to_numeric(
            df.Price.replace(r"[^\d.]", "", regex=True), errors="coerce"
        )

        # call functions to calculate total, 30% buffer, and grand total
        subtotal = calc_subtotal(df)
        thirty_percent = calc_thirty_percent(subtotal)
        grand_total = calc_grand_total(subtotal, thirty_percent)

        # create summary table
        summary_data = pd.DataFrame(
            {
                "Expense": ["Subtotal", "30% Buffer", "Grand Total"],
                "Price": [subtotal, thirty_percent, grand_total],
                "Notes": [
                    "Initial Estimate",
                    "Cause things are always WAY more expensive than you think",
                    "Sticker shock, eh? You CAN do this",
                ],
            }
        ).to_dict("records")

        return summary_data

    # downloads current budget as a csv
    @app.callback(
        Output("download-link", "data"),
        Input("save-button", "n_clicks"),
        State("budget-table", "data"),
        State("summary-table", "data"),
    )
    def save_data(n_clicks, budget_data, summary_data):
        """
        Downloads current budget as a csv if the save button is clicked.
        """
        # set n_clicks above 0, or it'll download on initial load
        if n_clicks > 0:
            budget_df = pd.DataFrame(budget_data)
            summary_df = pd.DataFrame(summary_data)

            # concatenate the df's
            df = pd.concat([budget_df, summary_df], ignore_index=True)

            # convert combined df to csv file
            csv_file = df.to_csv(index=False, encoding="utf-8")

            # create download link
            download_link = dict(
                content=csv_file, filename="travel_budget.csv", type="text/csv"
            )

            return download_link

    # updates donut chart
    @app.callback(
        Output("expense-donut-chart", "figure"),
        Input("budget-table", "data"),
        Input("summary-table", "data"),
        prevent_initial_call=True,
    )
    def update_donut_chart(budget_data, summary_data):
        """
        Updates donut chart based on the budget table data and summary table data.
        """
        # if budget_data is empty (initial load), return an empty fig
        if not budget_data:
            return go.Figure()

        # extract labels and values from the budget data
        labels = [row["Expense"] for row in budget_data]
        values = [row["Price"] for row in budget_data]

        # regex price strings to floats
        values = [float(re.sub(r"[^\d.]", "", value)) for value in values]

        # add 30% buffer from the summary data
        labels.append("Now 23.1% Buffer")
        buffer_value = [
            row["Price"] for row in summary_data if row["Expense"] == "30% Buffer"
        ][0]
        values.append(buffer_value)

        # calculate total and percentages
        total = sum(values)
        percentages = [value / total for value in values] if total != 0 else values

        # create fig
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=percentages,
                    text=values,
                    hole=0.5,
                    hovertemplate="%{label}:  $%{text:.2f}<extra></extra>",
                    textinfo="percent",
                )
            ],
            layout=go.Layout(
                title={
                    "text": "Expense Breakdown:  Hover/click for details",
                    "x": 0.5,
                    "xanchor": "center",
                },
                showlegend=True,  # False for mobile if I ever Heroku this
                annotations=[
                    dict(
                        x=0.5,
                        y=-0.1,
                        xanchor="center",
                        showarrow=False,
                        text=f"Total: ${total:.2f}",
                        xref="paper",
                        yref="paper",
                        font=dict(
                            size=20,
                        ),
                    )
                ],
            ),
        )

        return fig

    # initialize the app
    if __name__ == "__main__":
        app.run(debug=True)


def format_price(budget):
    """
    Format price from string to float, in case of user chichanery.
    """
    if "Price" in budget.columns:
        budget.Price = pd.to_numeric(
            budget.Price.replace(r"[^\d.]", "", regex=True), errors="coerce"
        )
        budget.Price = budget.Price.astype(float).map("${:,.2f}".format)
    return budget


def add_new_row(budget):
    """
    Add a new row to the budget table.
    """
    new_row = {"Expense": "", "Price": "$0.00", "Notes": ""}
    budget.loc[len(budget)] = new_row
    return budget


def calc_subtotal(df):
    """
    Calculate the subtotal of the budget.
    """
    df.Price = pd.to_numeric(df.Price, errors="coerce")
    df.Price = df.Price.astype(float)
    return df.Price.sum()


def calc_thirty_percent(subtotal):
    """
    Calculate the 30% buffer of the budget.
    """
    return 0.3 * subtotal


def calc_grand_total(subtotal, thirty_percent):
    """
    Calculate the grand total of the budget.
    """
    return subtotal + thirty_percent


if __name__ == "__main__":
    main()
