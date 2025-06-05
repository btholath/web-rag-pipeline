import random
from datetime import datetime, timedelta
import csv
import os

def generate_ford_trucks_dataset(num_records=500):
    models = [
        "Ford F-150", "Ford F-250 Super Duty", "Ford F-350 Super Duty",
        "Ford Ranger", "Ford Maverick", "Ford F-450 Super Duty",
        "Ford F-150 Lightning", "Ford F-650", "Ford F-750"
    ]
    colors = [
        "Oxford White", "Agate Black", "Antimatter Blue", "Rapid Red",
        "Stone Gray", "Carbonized Gray", "Iconic Silver"
    ]
    fuel_types = ["Gasoline", "Diesel", "Hybrid", "Electric"]
    transmission_types = ["Automatic", "Manual"]
    states = [
        "Texas", "California", "Florida", "Oklahoma", "Ohio",
        "Michigan", "Pennsylvania", "Georgia"
    ]

    dataset = []

    for _ in range(num_records):
        model = random.choice(models)
        color = random.choice(colors)
        fuel_type = random.choice(fuel_types)
        transmission = random.choice(transmission_types if model != "Ford F-150 Lightning" else ["Automatic"])
        price = round(random.uniform(28000, 95000), 2)  # Broader truck price range
        manufacture_date = datetime.now() - timedelta(days=random.randint(10, 730))
        sale_date = manufacture_date + timedelta(days=random.randint(7, 120))
        state = random.choice(states)
        mileage = round(random.uniform(5, 160000), 1)  # From new to high-mileage used trucks
        
        record = {
            "model": model,
            "color": color,
            "fuel_type": fuel_type,
            "transmission": transmission,
            "price": price,
            "manufacture_date": manufacture_date.strftime("%Y-%m-%d"),
            "sale_date": sale_date.strftime("%Y-%m-%d"),
            "state": state,
            "mileage": mileage
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

if __name__ == "__main__":
    ford_trucks_data = generate_ford_trucks_dataset()
    csv_file_path = save_to_csv(ford_trucks_data)
    print(f"Dataset has been saved to: {csv_file_path}")

    # Print the first 5 records as a sample
    for i, record in enumerate(ford_trucks_data[:5], 1):
        print(f"\nRecord {i}:")
        for key, value in record.items():
            print(f"  {key}: {value}")

    print(f"\nTotal records generated and saved: {len(ford_trucks_data)}")
