import pandas as pd
import pytest
from main import (
    format_price,
    add_new_row,
    calc_subtotal,
    calc_thirty_percent,
    calc_grand_total,
)


# Test format_price
def test_format_price():
    budget = pd.DataFrame({"Price": ["1000.00", "2000.00", "3000.00"]})
    expected_result = pd.DataFrame({"Price": ["$1,000.00", "$2,000.00", "$3,000.00"]})
    assert format_price(budget).equals(expected_result)
    budget = pd.DataFrame({"Price": ["$10.50", "$20.00", "$15.75"]})
    expected_result = pd.DataFrame({"Price": ["$10.50", "$20.00", "$15.75"]})
    assert format_price(budget).equals(expected_result)


# Test add_new_row
def test_add_new_row():
    budget = pd.DataFrame(
        {
            "Expense": ["Flight", "Hotel", "Food"],
            "Price": [1000.00, 2000.00, 500.00],
            "Notes": ["", "", ""],
        }
    )
    expected_result = pd.DataFrame(
        {
            "Expense": ["Flight", "Hotel", "Food", ""],
            "Price": [
                1000.00,
                2000.00,
                500.00,
                "$0.00",
            ],
            "Notes": ["", "", "", ""],
        }
    )
    assert add_new_row(budget).equals(expected_result)
    budget = pd.DataFrame(
        {
            "Expense": ["Item1", "Item2", "Item3"],
            "Price": [10.5, 20.0, 15.75],
            "Notes": ["Note1", "Note2", "Note3"],
        }
    )
    expected_result = pd.DataFrame(
        {
            "Expense": ["Item1", "Item2", "Item3", ""],
            "Price": [10.5, 20.0, 15.75, "$0.00"],
            "Notes": ["Note1", "Note2", "Note3", ""],
        }
    )
    assert add_new_row(budget).equals(expected_result)


# Test calc_subtotal
def test_calc_subtotal():
    budget = pd.DataFrame(
        {"Item": ["Flight", "Hotel", "Food"], "Price": [1000.00, 2000.00, 500.00]}
    )
    expected_result = 3500.00  # 1000.00 + 2000.00 + 500.00
    assert calc_subtotal(budget) == expected_result
    budget = pd.DataFrame(
        {
            "Expense": ["Item1", "Item2", "Item3"],
            "Price": [10.5, 20.0, 15.75],
            "Notes": ["Note1", "Note2", "Note3"],
        }
    )
    expected_subtotal = 46.25
    assert calc_subtotal(budget) == expected_subtotal


# Test calc_thirty_percent
def test_calc_thirty_percent():
    subtotal = 3500.00
    expected_result = 1050.00
    assert calc_thirty_percent(subtotal) == expected_result
    subtotal = 46.25
    thirty_percent = 13.875
    assert calc_thirty_percent(subtotal) == thirty_percent


# Test calc_grand_total
def test_calc_grand_total():
    subtotal = 3500.00
    thirty_percent = 1050.00
    expected_result = 4550.00
    assert calc_grand_total(subtotal, thirty_percent) == expected_result
    subtotal = 46.25
    thirty_percent = 13.875
    expected_grand_total = 60.125
    assert calc_grand_total(subtotal, thirty_percent) == expected_grand_total
