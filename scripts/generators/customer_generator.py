import json
import random
from pathlib import Path

TOTAL_CUSTOMERS = 100

class CustomerGenerator:

    @staticmethod
    def generate():

        base_dir = Path(__file__).resolve().parents[2]

        output_file = (
            base_dir
            / "source_systems"
            / "customer_api"
            / "customer_data.json"
        )

        first_names = [
            "Harshit", "Rahul", "Priya", "Sneha",
            "Amit", "Neha", "Rohan", "Anjali",
            "Karan", "Pooja"
        ]

        last_names = [
            "Sharma", "Verma", "Singh", "Patel",
            "Gupta", "Sinha", "Yadav", "Joshi"
        ]

        cities = [
            "Delhi",
            "Mumbai",
            "Bangalore",
            "Pune",
            "Hyderabad",
            "Chennai"
        ]

        memberships = [
            "Gold",
            "Silver",
            "Bronze"
        ]

        customers = []

        for customer_id in range(1, TOTAL_CUSTOMERS + 1):

            first = random.choice(first_names)
            last = random.choice(last_names)

            customers.append({
                "customer_id": customer_id,
                "first_name": first,
                "last_name": last,
                "email": f"{first.lower()}.{last.lower()}{customer_id}@retailhub.com",
                "city": random.choice(cities),
                "membership": random.choice(memberships)
            })

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as file:
            json.dump(customers, file, indent=4)

        print("✅ Customer data generated successfully.")