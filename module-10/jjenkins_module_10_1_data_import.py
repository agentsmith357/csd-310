"""
Author: Jelani Jenkins & Clint Scott
Date: 05/04/2025
Assignment: Module 10.1 - Create Table Script

write the .sql script to create the tables in MySQL, and populate each with at least 6 records
(fewer if noted in the case study, for example only three suppliers noted at Bacchus Winery). 
Write a python script that displays the data in each table (remember the movies example?),
and take a screenshot of the results of the script that displays the data in each table. 

"""

import mysql.connector
from dotenv import dotenv_values
from pathlib import Path
import os, sys

BASE_DIR = Path(__file__).resolve().parent.parent
ENV = Path(os.path.join(BASE_DIR, ".env"))

if os.path.exists(ENV):
    secrets = dotenv_values(ENV)
else:
    sys.exit("No .env file found.")


def reconnect_to_db():
    return mysql.connector.connect(**{"user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True})

def insert_data():
    conn = reconnect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO Department (Name) VALUES ('HR'), ('IT'), ('Operations'), ('Finance'), ('Sales'), ('Logistics');")

        cursor.execute("""
            INSERT INTO Employee (Name, DepartmentID, Position) VALUES
            ('Alice Smith', 1, 'Manager'),
            ('Bob Jones', 2, 'Developer'),
            ('Carol Lee', 3, 'Supervisor'),
            ('David Kim', 4, 'Analyst'),
            ('Eve Turner', 5, 'Sales Rep'),
            ('Frank Lin', 6, 'Coordinator');
        """)

        cursor.execute("""
            INSERT INTO EmployeeHours (EmployeeID, Week, HoursWorked) VALUES
            (1, '2025-04-28', 40),
            (2, '2025-04-28', 38),
            (3, '2025-04-28', 42),
            (4, '2025-04-28', 36),
            (5, '2025-04-28', 45),
            (6, '2025-04-28', 39);
        """)

        cursor.execute("INSERT INTO SupplyType (Description) VALUES ('Paper'), ('Ink'), ('Staples'), ('Binders'), ('Pens'), ('Markers');")

        cursor.execute("INSERT INTO Supplier (Name) VALUES ('OfficeMax'), ('Staples Inc.'), ('Amazon'), ('Walmart'), ('Office Depot'), ('Best Supplies');")

        cursor.execute("""
            INSERT INTO SupplyShipment (SupplierID, SupplyTypeID, Quantity, ExpectedDeliveryDate, ActualDeliveryDate) VALUES
            (1, 1, 100, '2025-05-05', '2025-05-04'),
            (2, 2, 200, '2025-05-06', NULL),
            (3, 3, 300, '2025-05-07', '2025-05-07'),
            (4, 4, 150, '2025-05-08', '2025-05-08'),
            (5, 5, 250, '2025-05-09', '2025-05-10'),
            (6, 6, 180, '2025-05-10', '2025-05-10');
        """)

        cursor.execute("""
            INSERT INTO SupplyInventory (SupplyTypeID, QuantityOnHand, LastUpdated) VALUES
            (1, 80, NOW()),
            (2, 150, NOW()),
            (3, 250, NOW()),
            (4, 100, NOW()),
            (5, 300, NOW()),
            (6, 90, NOW());
        """)

        cursor.execute("INSERT INTO Wine (Name, Type) VALUES ('Merlot', 'Red'), ('Chardonnay', 'White'), ('Rosé', 'Blush'), ('Cabernet', 'Red'), ('Sauvignon Blanc', 'White'), ('Zinfandel', 'Red');")

        cursor.execute("INSERT INTO Distributor (Name) VALUES ('Wine Co. A'), ('Grapes Galore'), ('Barrels & Bottles'), ('Vintage Vines'), ('Red & White LLC'), ('Cellar Select');")

        cursor.execute("""
            INSERT INTO WineOrders (DistributorID, WineID, Quantity, OrderDate, ShipDate, OrderStatus) VALUES
            (1, 1, 50, '2025-05-01', '2025-05-02', 'Shipped'),
            (2, 2, 75, '2025-05-01', NULL, 'Pending'),
            (3, 3, 100, '2025-05-02', '2025-05-03', 'Delivered'),
            (4, 4, 120, '2025-05-03', '2025-05-04', 'Shipped'),
            (5, 5, 90, '2025-05-04', NULL, 'Pending'),
            (6, 6, 110, '2025-05-05', '2025-05-06', 'Delivered');
        """)

        cursor.execute("""
            INSERT INTO WineInventory (WineID, QuantityOnHand, LastUpdated) VALUES
            (1, 120, NOW()),
            (2, 90, NOW()),
            (3, 60, NOW()),
            (4, 150, NOW()),
            (5, 75, NOW()),
            (6, 130, NOW());
        """)

        conn.commit()
        print("6 rows of data inserted into each table.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    insert_data()
