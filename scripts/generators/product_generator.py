import random
from pathlib import Path

import pandas as pd
TOTAL_PRODUCTS = 50

class ProductGenerator:

    @staticmethod
    def generate():

        base_dir = Path(__file__).resolve().parents[2]

        output_file = (
            base_dir
            / "source_systems"
            / "products_csv"
            / "products.csv"
        )

        products = [
            ("Laptop", "Electronics", "Dell"),
            ("Smartphone", "Electronics", "Samsung"),
            ("Keyboard", "Accessories", "Logitech"),
            ("Mouse", "Accessories", "Logitech"),
            ("Monitor", "Electronics", "LG"),
            ("Tablet", "Electronics", "Apple"),
            ("Printer", "Office", "HP"),
            ("Headphones", "Accessories", "Sony"),
            ("Webcam", "Accessories", "Logitech"),
            ("Speaker", "Electronics", "JBL")
        ]

        product_data = []

        for product_id in range(1, TOTAL_PRODUCTS + 1):

            product = random.choice(products)

            product_data.append({
                "product_id": product_id,
                "product_name": product[0],
                "category": product[1],
                "brand": product[2],
                "price": random.randint(500, 80000),
                "stock_status": random.choice(
                    ["In Stock", "Low Stock", "Out of Stock"]
                )
            })

        df = pd.DataFrame(product_data)

        output_file.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_file, index=False)

        print("✅ Product data generated successfully.")