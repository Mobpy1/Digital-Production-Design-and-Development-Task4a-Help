import pandas as pd
import matplotlib.pyplot as plt

def openfile():
    db = pd.read_csv('car_sales_data.csv')

    return db



#MENU SIMPLE
def menu():
    print("###########################################################################################################")
    print("1: All Car Sales                      // Contains Graph For Sales Over Time")
    print("2: Car Sales By Specific Date         // Contains Bar Chart For Sales By Each Employee On Date")
    print("3: Car Sales by a range of Date       // Contains Graph For Sales Over Selected Dates")
    print("4: Car Sales by Employee              // Contains Graph For Sales By Selected Employee")
    print("5: Summary Of all Employees           // Contains Bar Chart For Sales By All Employees")
    print("6: EXIT")
    print("###########################################################################################################")

    choice = input("\n Please Select an option :")
    print("\n")
    
    try:
        choice = int(choice)
        if 0 < choice < 7:
            return choice
        else:
            print("Invalid Input. Please select a number between 1 and 6.")
            return 'FAIL'
    except ValueError:
        print("Invalid Input. Please enter a valid number.")
        return 'FAIL'


# PLOT EMPLOYEE SALES  WORKS FOR 2 OPTIONS     OPTION 2 AND OPTION 5    REVISE THIS
def plot_employee_sales(filtered_data):
    employee_sales = filtered_data.groupby('Sales_Person').agg(
        total_sales=('Price', 'sum'),
        total_cars_sold=('Sale_ID', 'count')
    ).reset_index()
    
    plt.figure(figsize =(10,6))
    plt.bar(employee_sales['Sales_Person'],employee_sales['total_sales'], color= 'skyblue')
    plt.xlabel("Employee")
    plt.ylabel("Total Sales")
    plt.title("Total Sales by Employee")
    plt.xticks(rotation=45,ha ='right')
    plt.tight_layout()
    plt.show()


# PLOT SALES OVER TIME IN GRAPH WORKS FOR 2 OPTIONS     OPTION 1 AND OPTION 3    REVISE THIS  
def plot_sales_over_time(db):
    # Line graph for sales over time (if data spans across dates)
    db.loc[:,'Date'] = pd.to_datetime(db['Date'])
    daily_sales = db.groupby('Date').agg({'Price': 'sum'}).reset_index()

    plt.figure(figsize=(10,6))
    plt.plot(daily_sales['Date'], daily_sales['Price'], marker='o', linestyle='-', color='green')
    plt.xlabel('Date')
    plt.ylabel('Total Sales ($)')
    plt.title('Sales Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_sales_over_time_individual_employee(db,employee):
    # Line graph for sales over time (if data spans across dates)
    db.loc[:,'Date'] = pd.to_datetime(db['Date'])
    daily_sales = db.groupby('Date').agg({'Price': 'sum'}).reset_index()

    plt.figure(figsize=(10,6))
    plt.plot(daily_sales['Date'], daily_sales['Price'], marker='o', linestyle='-', color='green')
    plt.xlabel('Date')
    plt.ylabel('Total Sales ($)')
    plt.title(f'Sales Over Time By {employee}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



def reading_data(choice, db):   # TOTAL CARS SOLD
    if choice == 1:
        total_sales = db['Price'].sum()  
        total_cars = len(db)
        
        print(f"Total Sales Amount: ${total_sales}")
        print(f"Total Cars Sold: {total_sales}\n\n")
        plot_sales_over_time(db)


    elif choice == 2:   #NORMAL SINGULAR DATE
        print(db["Date"])
        date = input("Enter Date (YYYY-MM-DD) to filter sales : ")
        filtered_data = db[db['Date'] == date]
        total_cars = len(filtered_data)
        total_sales = filtered_data['Price'].sum()

        if filtered_data.empty:
            print("No Data\n\n")
        else:
            print(filtered_data)
            print(f"\nTotal Sales Amount: {total_sales}")
            print(f"Total Cars Sold: {total_cars}\n\n")
            plot_employee_sales(filtered_data)

    elif choice == 3:         # DATE RANGE THIS WILL BE NEEDED USING pd.to_dattime FUNCTION REMEMBER THIS
        # Sales by Date Range
        print(db['Date'])
        print("\nEnter the Date Range to filter sales:")
        
        start_date = input("Enter Start Date (YYYY-MM-DD): ")
        end_date = input("Enter End Date (YYYY-MM-DD): ")

        db['Date'] = pd.to_datetime(db['Date'])
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Correct way to filter by date range
        filtered_data = db[(db['Date'] >= start_date) & (db['Date'] <= end_date)]

        if filtered_data.empty:
            print("No Data\n\n")
        else:
            print(filtered_data)
            print(f"\nTotal Sales Amount: ${filtered_data['Price'].sum()}")
            print(f"Total Cars Sold: {len(filtered_data)}\n\n")
            plot_sales_over_time(filtered_data)


    elif choice == 4:   # SELECT EMPLOYEES
        employee = input("Enter Employee : ")
        
        filtered_data = db[db['Sales_Person'].str.lower() == employee.lower()]
    
        Total_Employee_Sales = filtered_data['Price'].sum()
        Total_Cars_Sold = len(filtered_data)

        if filtered_data.empty:
            print( "No Employee Data Found\n\n" )
        else:
            print(filtered_data) 
            print(f"\nTotal Cars Sold By {employee} = {Total_Cars_Sold}")
            print(f"Total Sales By {employee}= ${Total_Employee_Sales}\n\n")
            plot_sales_over_time_individual_employee(filtered_data,employee)
        
            

    elif choice == 5:   # Summary of all Employees
        print("\nCar Models and Sales by Employee:\n")
        
        
        
        # Now aggregate the data for all employees
        
        employee_sales = db.groupby("Sales_Person").agg(
            total_sales=('Price', 'sum'),
            Total_Cars_Sold=('Sale_ID','count')
        ).reset_index()
        
        if employee_sales.empty:
            print("No Data Available\n\n")
        else:
            print(employee_sales)
            plot_employee_sales(db)
        
        print("\n\n")

    elif choice == 6:   # exit
        print("EXITING\n\n")
        return 0

def main():
    db = openfile()
    flag = True

    
    while flag:
        choice = menu()

        if choice == 'FAIL':
            continue

        if reading_data(choice, db) == 0:
            flag = False

        
main()