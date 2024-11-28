import pandas as pd
import matplotlib.pyplot as plt

def openfile():
    """
    Reads the car sales data from a CSV file and returns it as a pandas DataFrame.
    
    Returns:
        pd.DataFrame: A DataFrame containing the car sales data.
    """
    db = pd.read_csv('car_sales_data.csv')
    return db


def menu():
    """
    Displays a simple text-based menu to the user and prompts them to select an option.

    Returns:
        int or str: Returns the user's choice as an integer if valid, otherwise returns 'FAIL' if the input is invalid.
    """
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


def plot_employee_sales(filtered_data):
    """
    Plots a bar chart showing total sales by employee.

    Args:
        filtered_data (pd.DataFrame): The DataFrame containing sales data filtered by date or other criteria.
    """
    employee_sales = filtered_data.groupby('Sales_Person').agg(
        total_sales=('Price', 'sum'),
        total_cars_sold=('Sale_ID', 'count')
    ).reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.bar(employee_sales['Sales_Person'], employee_sales['total_sales'], color='skyblue')
    plt.xlabel("Employee")
    plt.ylabel("Total Sales")
    plt.title("Total Sales by Employee")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def plot_sales_over_time(db):
    """
    Plots a line graph showing sales over time.

    Args:
        db (pd.DataFrame): The DataFrame containing car sales data.
    """
    db['Date'] = pd.to_datetime(db['Date'])
    daily_sales = db.groupby('Date').agg({'Price': 'sum'}).reset_index()

    plt.figure(figsize=(10, 6))
    plt.plot(daily_sales['Date'], daily_sales['Price'], marker='o', linestyle='-', color='green')
    plt.xlabel('Date')
    plt.ylabel('Total Sales ($)')
    plt.title('Sales Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_sales_over_time_individual_employee(db, employee):
    """
    Plots a line graph showing sales over time for a specific employee.

    Args:
        db (pd.DataFrame): The DataFrame containing car sales data.
        employee (str): The name of the employee to filter the sales data.
    """
    db['Date'] = pd.to_datetime(db['Date'])
    daily_sales = db.groupby('Date').agg({'Price': 'sum'}).reset_index()

    plt.figure(figsize=(10, 6))
    plt.plot(daily_sales['Date'], daily_sales['Price'], marker='o', linestyle='-', color='green')
    plt.xlabel('Date')
    plt.ylabel('Total Sales ($)')
    plt.title(f'Sales Over Time By {employee}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def reading_data(choice, db):
    """
    Handles the user's menu choice and displays relevant data or plots based on the choice.

    Args:
        choice (int): The user's choice from the menu.
        db (pd.DataFrame): The DataFrame containing car sales data.

    Returns:
        int: Returns 0 to indicate the user chose to exit, otherwise returns None.
    """
    if choice == 1:
        # Option 1: Display total sales and plot sales over time.
        total_sales = db['Price'].sum()
        total_cars = len(db)
        print(f"Total Sales Amount: ${total_sales}")
        print(f"Total Cars Sold: {total_cars}\n\n")
        plot_sales_over_time(db)

    elif choice == 2:
        # Option 2: Filter sales by a specific date and display employee sales.
        print(db["Date"])
        date = input("Enter Date (YYYY-MM-DD) to filter sales: ")
        filtered_data = db[db['Date'] == date]
        total_cars = len(filtered_data)
        total_sales = filtered_data['Price'].sum()

        if filtered_data.empty:
            print("No Data\n\n")
        else:
            print(filtered_data)
            print(f"\nTotal Sales Amount: ${total_sales}")
            print(f"Total Cars Sold: {total_cars}\n\n")
            plot_employee_sales(filtered_data)

    elif choice == 3:
        # Option 3: Filter sales by a date range and display sales over time.
        print(db['Date'])
        print("\nEnter the Date Range to filter sales:")
        start_date = input("Enter Start Date (YYYY-MM-DD): ")
        end_date = input("Enter End Date (YYYY-MM-DD): ")

        db['Date'] = pd.to_datetime(db['Date'])
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_data = db[(db['Date'] >= start_date) & (db['Date'] <= end_date)]

        if filtered_data.empty:
            print("No Data\n\n")
        else:
            print(filtered_data)
            print(f"\nTotal Sales Amount: ${filtered_data['Price'].sum()}")
            print(f"Total Cars Sold: {len(filtered_data)}\n\n")
            plot_sales_over_time(filtered_data)

    elif choice == 4:
        # Option 4: Display sales for a specific employee.
        employee = input("Enter Employee: ")
        filtered_data = db[db['Sales_Person'].str.lower() == employee.lower()]
        total_employee_sales = filtered_data['Price'].sum()
        total_cars_sold = len(filtered_data)

        if filtered_data.empty:
            print("No Employee Data Found\n\n")
        else:
            print(filtered_data)
            print(f"\nTotal Cars Sold By {employee} = {total_cars_sold}")
            print(f"Total Sales By {employee} = ${total_employee_sales}\n\n")
            plot_sales_over_time_individual_employee(filtered_data, employee)

    elif choice == 5:
        # Option 5: Display a summary of sales by all employees.
        print("\nCar Models and Sales by Employee:\n")
        employee_sales = db.groupby("Sales_Person").agg(
            total_sales=('Price', 'sum'),
            total_cars_sold=('Sale_ID', 'count')
        ).reset_index()

        if employee_sales.empty:
            print("No Data Available\n\n")
        else:
            print(employee_sales)
            plot_employee_sales(db)

    elif choice == 6:
        # Option 6: Exit the program.
        print("EXITING\n\n")
        return 0


def main():
    """
    Main function to run the car sales data analysis program.
    """
    db = openfile()
    flag = True

    while flag:
        choice = menu()

        if choice == 'FAIL':
            continue

        if reading_data(choice, db) == 0:
            flag = False


if __name__ == "__main__":
    main()
