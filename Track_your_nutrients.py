import requests
from cProfile import label
from dataclasses import dataclass
from secrets import choice
from tkinter import image_types
from turtle import width
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector


age = int(input("Enter your age in years: "))
weight = float(input("Enter your weight in kilograms: "))
height = float(input("Enter your height in centimeters: "))

# Calculate basal metabolic rate (BMR) using the Mifflin-St Jeor equation
bmr = 10 * weight + 6.25 * height - 5 * age + 5

# Calculate daily caloric needs based on activity level
activity_level = input("Enter your activity level (sedentary, lightly active, moderately active, very active): ")
if activity_level == "sedentary":
    daily_calories = bmr * 1.2
elif activity_level == "lightly active":
    daily_calories = bmr * 1.375
elif activity_level == "moderately active":
    daily_calories = bmr * 1.55
elif activity_level == "very active":
    daily_calories = bmr * 1.725
else:
    print("Invalid activity level. Please try again.")
    exit()

# Calculate recommended nutrient intakes based on caloric needs
protein_grams = daily_calories * 0.15 / 4
fats_grams = daily_calories * 0.25 / 9
carbs_grams = daily_calories * 0.6 / 4

# Print results
print("Based on your age, weight, height, and activity level, you need approximately", int(daily_calories), "calories per day.")
print("You should aim to consume around", int(protein_grams), "grams of protein, ", int(fats_grams), "grams of fat, and", int(carbs_grams), "grams of carbohydrates per day.")



mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Naruto",
        )

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE nutritions")
mycursor.execute("USE nutritions")
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS nutrition (
        sr_no INT AUTO_INCREMENT PRIMARY KEY,
        Food VARCHAR(255),
        calories FLOAT,
        protein FLOAT,
        carbs FLOAT,
        fat FLOAT
    )
""")


today=[]

done = False
while not done:

    print(""""
    (1) Add a new food
    (2) Visualize progress
    (q) Quit
    """)

    choice = input("Choose an option : ")
    if choice == '1':
        APP_ID = "f94e7bfc" 
        API_KEY = "0a873f3cc2aa3543f07e745d29bf6daa" 
        url = "https://api.nutritionix.com/v1_1/search/" + input("Enter food item: ") + "?results=0:1&fields=item_name,nf_calories,nf_total_fat,nf_protein,nf_total_carbohydrate&appId=" + APP_ID + "&appKey=" + API_KEY

        response = requests.get(url)
        data = response.json()
        
        if data['hits']:
        
            food = data['hits'][0]['fields']['item_name']
            calories = data['hits'][0]['fields']['nf_calories']
            fat = data['hits'][0]['fields']['nf_total_fat']
            protein = data['hits'][0]['fields']['nf_protein']
            carbs = data['hits'][0]['fields']['nf_total_carbohydrate']
            print(f"Nutrition information for {food}:")
            print(f"Calories: {calories}")
            print(f"Fat: {fat}g")
            print(f"Protein: {protein}g")
            print(f"Carbohydrates: {carbs}g")
            calorie_sum=sum(food.calories for food in today)
            protein_sum=sum(food.protein for food in today)
            fats_sum=sum(food.fat for food in today)
            carbs_sum=sum(food.carbs for food in today)
            mycursor = mydb.cursor()
            sql = "INSERT INTO nutrition (Food, calories, fat, protein, carbs) VALUES (%s, %s, %s, %s, %s)"
            val = (food, calories, fat, protein, carbs)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "row inserted.")
        else:
            print("Food item not found")

    elif choice == '2':
                       
        calories_goal = [daily_calories] * 4  
        calories_intake = [calories] * 4  
        protein_grams = [protein_grams] * 4  
        protein_intake = [protein] * 4  
        fats_goal = [fats_grams] * 4  
        fats_intake = [fat] * 4  
        carbs_grams = [carbs_grams] * 4  
        carbs_intake = [carbs] * 4  


        
        labels = ['Group 1']
        bar_width = 0.15
        x = np.arange(len(labels))
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - 3*bar_width/2, calories_goal, bar_width, label='Calories Goal')
        rects2 = ax.bar(x - bar_width/2, protein_grams, bar_width, label='Protein Goal')
        rects3 = ax.bar(x + bar_width/2, fats_goal, bar_width, label='Fats Goal')
        rects4 = ax.bar(x + 3*bar_width/2, carbs_grams, bar_width, label='Carbs Goal')
        rects5 = ax.bar(x - 3*bar_width/2, calories_intake, bar_width, label='Calories Intake')
        rects6 = ax.bar(x - bar_width/2, protein_intake, bar_width, label='Protein Intake')
        rects7 = ax.bar(x + bar_width/2, fats_intake, bar_width, label='Fats Intake')
        rects8 = ax.bar(x + 3*bar_width/2, carbs_intake, bar_width, label='Carbs Intake')      
        ax.set_xlabel('Nutrient Goals vs. Actual Intake')
        ax.set_ylabel('Amount')
        ax.set_title('Nutrient Goals vs. Actual Intake')        
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        plt.savefig('graph.png')
        plt.show()
        

        
    elif choice == 'q':
        done = True