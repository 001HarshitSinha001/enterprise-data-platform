import random
from pathlib import Path

import pandas as pd
TOTAL_PRODUCTS = 50

class InventoryGenerator:

    @staticmethod
    def generate():

        base_dir = Path(__file__).resolve().parents[2]

        output_file = (
            base_dir
            / "source_systems"
            / "inventory_excel"
            / "inventory.xlsx"
        )

        warehouses = [
            "Delhi",
            "Mumbai",
            "Bangalore",
            "Hyderabad",
            "Chennai"
        ]

        inventory = []

        for product_id in range(1, TOTAL_PRODUCTS + 1):

            inventory.append({
                "product_id": product_id,
                "warehouse": random.choice(warehouses),
                "quantity": random.randint(10, 500),
                "reorder_level": random.randint(20, 100)
            })

        df = pd.DataFrame(inventory)

        output_file.parent.mkdir(parents=True, exist_ok=True)

        df.to_excel(output_file, index=False)

        print("✅ Inventory data generated successfully.")