# import dependencies
from dash import Dash, dcc, html, dash_table, callback, Input, Output
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
            # div to contain budget table
            html.Div(id="budget"),
            dash_table.DataTable(id="budget-table"),
            dash_table.DataTable(id="summary-table", columns=[
                {"name": "Expense", "id": "Expense"},
                {"name": "Price", "id": "Price"},
                {"name": "Notes", "id": "Notes"},
            ]),
            html.Div(id="hidden-div", style={"display": "none"}),
        ]
    )

    # decorator to update budget template
    @app.callback(
        Output("budget-table", "data"),
        Output("budget-table", "columns"),
        Output("summary-table", "data"),
        Output("hidden-div", "children"),
        Input("radio-buttons", "value"),
        Input("budget-table", "data_previous"),
        # prevent_initial_call=True,
    )
    def update_budget(button_chosen, data_previous):
        budget = pd.read_csv(f"./resources/{button_chosen.replace(' ', '_')}.csv")
        columns = [{"name": col, "id": col, "editable": True} for col in budget.columns]

        if data_previous:
            df_temp = pd.DataFrame(data_previous)

            total = calc_total(df_temp)
            thirty_percent = calc_thirty_percent(total)
            grand_total = calc_grand_total(total, thirty_percent)

            df_temp.loc[len(df_temp) - 3, "Price"] = total
            df_temp.loc[len(df_temp) - 2, "Price"] = thirty_percent
            df_temp.loc[len(df_temp) - 1, "Price"] = grand_total

            summary_data = df_temp.iloc[-3:, :].to_dict("records")
            hidden_div_content = df_temp.iloc[:-3, :].to_json(orient="split")

            return [df_temp.to_dict("records"), columns, summary_data, hidden_div_content]

        return [budget.to_dict("records"), columns, [], None]

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
