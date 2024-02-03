# Python Travel Budget with Dash demo

Development on this project has stopped.

## Table of Contents

- [Description](#description)
- [Usage](#usage)
- [Gallery](#gallery)
- [Rogues Gallery](#rogues-gallery)
- [References](#references)
- [Acknowledgements](#acknowledgements)
- [Author](#author)

## Description

This project was developed as a final project for [cs50's Introduction to Programming with Python](https://cs50.harvard.edu/python/2022/weeks/0/). It provides a dashboard for building and exporting travel budgets, and includes example budgets and a donut chart for visualization.

This project evolved from a few base requirements, namely that the main program must be a python project, rather obvious, with at least three functions outside of main that had accompanying unit tests in a separate file. This obviously impacted the design.

As I've mostly focused on data science / analysis / visualization, coming up with a good, clean, command line python project stumped me for a bit. I decided I want to talk about travel stories - at least I'd enjoy the subject matter, and amuse my friends and family who've been subjected to my budget spreadsheets (and then thanked me for the awesome vacations). I replicated my spreadsheets, building a budget app that ran from the command line using tabulate and Pandas DataFrames to display info on the command line.

That lasted a hot second before I tossed the idea and went with Dash from Plotly. It was something I'd never used before - bonus points for learning something new! Programming html from python intrigued me. I could build a python project that had the user-friendliness of a webpage, much more visually appealing than tabulate boxes printing to the terminal. It also vastly increased the amount of time that I spent on this project.

I hit a lot of walls along the way on this one. But Dash has far friendly documentation that Python, so it wasn't too hard to learn. Another day, another five billion errors.

Ideas for the future: I would clean up the formatting a lot, add options for what type of file is exports (Excel, Google Sheets, HTML, even SQL or JSON if I wanna go crazy). Maybe change the donut chart to a bar chart. Add an option to load a file.

Honestly, I'd love to set up an auto-generated budget, using api's to places like skyscanner (for flight info). But that's a bit ambitious - where can you web scrape an estimate for the cost of meals in random places? It requires thought.

So there's my little toy, an ode to my friends and many adventures, of the global AND the computational variety. Check out some images below!

## Usage

Launch the `main.py` dash app from the command line. Peruse the radio buttons at the top to get ideas for how to assemble a travel budget. A modal will prevent a user from accidentally leaving a budget in progress. The large `Add a Row` and `Delete the Bottom Row` buttons will add or subtract a row from the bottom of the table. Sneakily, there are small x's on the right that will allow a user to delete rows from the middle of the table.

The budget will constantly update the lower table, summarizing the grand total and adjusting the donut chart.

Clicking the `Save and Download` button will convert the budget to a csv and download to the user's hard drive.

Run `pytest` from the command line to see the results of the unit tests contained in `test_main.py`.

## Gallery

Template:

![Template](./assets/images/template.png)

Machu Picchu Budget:

![Machu Picchu Budget](./assets/images/machu_picchu.png)

Machu Picchu Summary and Plot:

![Machu Picchu Summary and Plot](./assets/images/machu_picchu_graph.png)

Saint John Budget:

![Saint John Budget](./assets/images/STJ_weekend.png)

Saint John Summary and Plot:

![Saint John Summary and Plot](./assets/images/STJ_weekend_graph.png)

## Rogues Gallery

![Saint John](./assets/images/STJ%20goofy.jpg)

![Stairs of Death](./assets/images/mp%20stairs%20of%20death.jpg)

![Isle of Skye](./assets/images/Isle%20of%20Skye.jpg)

![Namibia](./assets/images/Namibia.jpg)

![Edinburgh Castle](./assets/images/Edinburgh%20Castle.jpg)

![Stereotypical Machu Picchu](./assets/images/mp.HEIC)

## References

Sample budgets provided by author

## Acknowledgements

Much gratitude to the cs50 team, for helping this autodidact learn to code.

And to the friends and family who've journeyed with me.

## Author

Bryan Johns, February 2024
