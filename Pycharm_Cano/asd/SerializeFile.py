import csv

import pandas as pd

import Motorcycle

def saveMotorcycle(filename, motorcycle):
    with open(filename, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([motorcycle.ID, motorcycle.brand, motorcycle.model,
                         motorcycle.year, motorcycle.price, motorcycle.posFile])

# Modify the function calls accordingly in your code.

def modifyMotorcycle(filename, motorcycle):
    try:
        data = pd.read_csv(filename)
        row_index = data.index[data['PosFile'] == motorcycle.posFile].tolist()
        if row_index:
            row_index = row_index[0]
            data.at[row_index, 'Brand'] = motorcycle.brand
            data.at[row_index, 'Model'] = motorcycle.model
            data.at[row_index, 'Year'] = motorcycle.year
            data.at[row_index, 'Price'] = motorcycle.price
            data.to_csv(filename, index=False)
        else:
            print("Motorcycle not found in the CSV file.")
    except pd.errors.EmptyDataError:
        print("The CSV file is empty.")
    except FileNotFoundError:
        print(f"The file {filename} was not found.")

def readMotorcycle(filename, motorcycle_list):
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                motorcycle_list.append(
                    Motorcycle.Motorcycle(row['ID'], row['Brand'], row['Model'], row['Year'], row['Price'], row['pos'])
                )
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
