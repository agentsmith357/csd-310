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
    return mysql.connector.connect(**{
        "user": secrets["USER"],
        "password": secrets["PASSWORD"],
        "host": secrets["HOST"],
        "database": secrets["DATABASE"],
        "raise_on_warnings": True
    })

def create_tables():
    conn = reconnect_to_db()
    cursor = conn.cursor()

    try:
        # Drop tables if they exist
        drop_order = [
            "WineInventory", "WineOrders", "Distributor", "Wine",
            "SupplyInventory", "SupplyShipment", "Supplier", "SupplyType",
            "EmployeeHours", "Employee", "Department"
        ]
        for table in drop_order:
            cursor.execute(f"DROP TABLE IF EXISTS {table};")

        # Create tables
        cursor.execute("""
            CREATE TABLE Department (
                DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE Employee (
                EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                DepartmentID INT,
                Position VARCHAR(255),
                FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
            );
        """)
        cursor.execute("""
            CREATE TABLE EmployeeHours (
                RecordID INT AUTO_INCREMENT PRIMARY KEY,
                EmployeeID INT,
                Week DATE,
                HoursWorked DECIMAL(5,2),
                FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
            );
        """)
        cursor.execute("""
            CREATE TABLE SupplyType (
                SupplyTypeID INT AUTO_INCREMENT PRIMARY KEY,
                Description VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE Supplier (
                SupplierID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE SupplyShipment (
                ShipmentID INT AUTO_INCREMENT PRIMARY KEY,
                SupplierID INT,
                SupplyTypeID INT,
                Quantity INT,
                ExpectedDeliveryDate DATE,
                ActualDeliveryDate DATE,
                FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
                FOREIGN KEY (SupplyTypeID) REFERENCES SupplyType(SupplyTypeID)
            );
        """)
        cursor.execute("""
            CREATE TABLE SupplyInventory (
                SupplyInventoryID INT AUTO_INCREMENT PRIMARY KEY,
                SupplyTypeID INT,
                QuantityOnHand INT,
                LastUpdated TIMESTAMP,
                FOREIGN KEY (SupplyTypeID) REFERENCES SupplyType(SupplyTypeID)
            );
        """)
        cursor.execute("""
            CREATE TABLE Wine (
                WineID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255),
                Type VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE Distributor (
                DistributorID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE WineOrders (
                OrderID INT AUTO_INCREMENT PRIMARY KEY,
                DistributorID INT,
                WineID INT,
                Quantity INT,
                OrderDate DATE,
                ShipDate DATE,
                OrderStatus VARCHAR(100),
                FOREIGN KEY (DistributorID) REFERENCES Distributor(DistributorID),
                FOREIGN KEY (WineID) REFERENCES Wine(WineID)
            );
        """)
        cursor.execute("""
            CREATE TABLE WineInventory (
                WineInventoryID INT AUTO_INCREMENT PRIMARY KEY,
                WineID INT,
                QuantityOnHand INT,
                LastUpdated TIMESTAMP,
                FOREIGN KEY (WineID) REFERENCES Wine(WineID)
            );
        """)

        conn.commit()
        print("Tables dropped and recreated successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()