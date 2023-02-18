# Calorie-tracker-with-DBMS

Nutrition Tracker
This is a Python script to calculate daily caloric and nutrient needs based on inputted age, weight, height, and activity level. It also allows the user to add a new food item and visualize progress towards their daily nutrient goals.

Dependencies
This script depends on the following Python packages:

requests
dataclasses
secrets
tkinter
turtle
numpy
matplotlib
mysql-connector-python
You can install them all at once by running:

pip install requests dataclasses secrets tkinter turtle numpy matplotlib mysql-connector-python


Usage

First you must have MYSQL installed on your computer and after that you much change the password to connect with MYSQL.

Run the script and enter your age, weight, and height when prompted. Then, enter your activity level from the options given: sedentary, lightly active, moderately active, or very active.

The script will then calculate your daily caloric needs and recommended nutrient intakes based on your input.

To add a new food item, choose option 1 when prompted and enter the name of the food item. The script will use the Nutritionix API to fetch the nutrition information for that food item and print it to the console. It will also insert the information into a MySQL database named nutritions in a table named nutrition.

To visualize your progress towards your daily nutrient goals, choose option 2 when prompted. The script will plot a bar chart showing your daily caloric goal, daily protein goal, daily fat goal, and daily carbohydrate goal, as well as your current intake for each nutrient.

To quit the script, choose option q when prompted.
