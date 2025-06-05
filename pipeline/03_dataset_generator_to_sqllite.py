import random
from datetime import datetime, timedelta
import csv
import os
import sqlite3

def generate_ford_trucks_dataset(num_records=5000):
    models = {
        "Ford F-150": {"price_range": (34000, 78000), "mileage_range": (10, 180000), "fuel_types": ["Gasoline", "Hybrid", "Electric"]},
        "Ford F-150 Lightning": {"price_range": (55000, 97000), "mileage_range": (8, 120000), "fuel_types": ["Electric"]},
        "Ford Ranger": {"price_range": (28000, 44000), "mileage_range": (10, 160000), "fuel_types": ["Gasoline"]},
        "Ford Maverick": {"price_range": (24000, 39000), "mileage_range": (5, 90000), "fuel_types": ["Gasoline", "Hybrid"]},
        "Ford F-250 Super Duty": {"price_range": (45000, 99000), "mileage_range": (12, 220000), "fuel_types": ["Gasoline", "Diesel"]},
        "Ford F-350 Super Duty": {"price_range": (50000, 105000), "mileage_range": (10, 250000), "fuel_types": ["Gasoline", "Diesel"]},
        "Ford F-450 Super Duty": {"price_range": (57000, 115000), "mileage_range": (10, 260000), "fuel_types": ["Diesel"]},
        "Ford F-650": {"price_range": (60000, 125000), "mileage_range": (10, 180000), "fuel_types": ["Diesel"]},
        "Ford F-750": {"price_range": (65000, 140000), "mileage_range": (8, 180000), "fuel_types": ["Diesel"]},
    }
    colors = [
        "Oxford White", "Agate Black", "Antimatter Blue", "Rapid Red",
        "Stone Gray", "Carbonized Gray", "Iconic Silver"
    ]
    transmission_types = ["Automatic", "Manual"]
    states = [
        "Texas", "California", "Florida", "Oklahoma", "Ohio",
        "Michigan", "Pennsylvania", "Georgia"
    ]
    variants = ["XL", "XLT", "Lariat", "Platinum", "King Ranch", "Limited", "Tremor"]

    dataset = []

    for _ in range(num_records):
        model = random.choice(list(models.keys()))
        color = random.choice(colors)
        fuel_type = random.choice(models[model]["fuel_types"])
        transmission = random.choice(["Automatic"] if model == "Ford F-150 Lightning" or fuel_type == "Electric" else transmission_types)
        variant = random.choice(variants)
        
        price_range = models[model]["price_range"]
        price = round(random.uniform(*price_range), 2)
        
        mileage_range = models[model]["mileage_range"]
        mileage = round(random.uniform(*mileage_range), 1)
        
        manufacture_date = datetime.now() - timedelta(days=random.randint(1, 1460))  # Up to 4 years old
        sale_date = manufacture_date + timedelta(days=random.randint(1, 180))  # Up to 6 months to sell
        state = random.choice(states)
        
        # Engine/Battery nuanced fields
        if fuel_type == "Electric":
            engine_capacity = 0
            battery_capacity = round(random.uniform(95, 130), 1)  # kWh for F-150 Lightning
            charging_time = round(random.uniform(0.75, 10), 1)  # Hours
        else:
            battery_capacity = 0
            charging_time = 0
            if fuel_type == "Diesel":
                engine_capacity = round(random.uniform(6.2, 7.3), 1)  # Litre, Powerstroke
            elif fuel_type == "Gasoline":
                engine_capacity = round(random.uniform(2.3, 7.3), 1)  # Litre
            else:  # Hybrid
                engine_capacity = round(random.uniform(2.3, 3.5), 1)
        
        seating_capacity = 5 if model not in ["Ford F-250 Super Duty", "Ford F-350 Super Duty", "Ford F-450 Super Duty", "Ford F-650", "Ford F-750"] else 6
        ground_clearance = round(random.uniform(200, 250), 1)
        bed_length = round(random.uniform(5.5, 8), 1)  # feet
        towing_capacity = random.randint(5000, 37000)  # lbs

        record = {
            "model": model,
            "variant": variant,
            "color": color,
            "fuel_type": fuel_type,
            "transmission": transmission,
            "price": price,
            "manufacture_date": manufacture_date.strftime("%Y-%m-%d"),
            "sale_date": sale_date.strftime("%Y-%m-%d"),
            "state": state,
            "mileage": mileage,
            "engine_capacity": engine_capacity,
            "battery_capacity": battery_capacity,
            "charging_time": charging_time,
            "seating_capacity": seating_capacity,
            "ground_clearance": ground_clearance,
            "bed_length": bed_length,
            "towing_capacity": towing_capacity
        }
        dataset.append(record)
    
    return dataset

def save_to_csv(data, filename="./data/ford_trucks_data.csv"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return file_path

def save_to_sqlite(data, db_name="./data/ford_trucks_data.db"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, db_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ford_trucks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        variant TEXT,
        color TEXT,
        fuel_type TEXT,
        transmission TEXT,
        price REAL,
        manufacture_date TEXT,
        sale_date TEXT,
        state TEXT,
        mileage REAL,
        engine_capacity REAL,
        battery_capacity REAL,
        charging_time REAL,
        seating_capacity INTEGER,
        ground_clearance REAL,
        bed_length REAL,
        towing_capacity INTEGER
    )
    ''')
    for record in data:
        cursor.execute('''
        INSERT INTO ford_trucks (
            model, variant, color, fuel_type, transmission, price, manufacture_date, sale_date,
            state, mileage, engine_capacity, battery_capacity, charging_time, seating_capacity,
            ground_clearance, bed_length, towing_capacity
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(record.values()))
    conn.commit()
    conn.close()
    return db_path

# Generate the dataset
ford_trucks_data = generate_ford_trucks_dataset(5000)

# Save the dataset to a CSV file
csv_file_path = save_to_csv(ford_trucks_data)

# Save the dataset to a SQLite database
db_file_path = save_to_sqlite(ford_trucks_data)

print(f"Dataset has been saved to CSV: {csv_file_path}")
print(f"Dataset has been saved to SQLite database: {db_file_path}")

# Print the first 5 records as a sample
for i, record in enumerate(ford_trucks_data[:5], 1):
    print(f"\nRecord {i}:")
    for key, value in record.items():
        print(f"  {key}: {value}")

print(f"\nTotal records generated and saved: {len(ford_trucks_data)}")
