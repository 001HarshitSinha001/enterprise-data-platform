from scripts.generators.customer_generator import CustomerGenerator
from scripts.generators.product_generator import ProductGenerator
from scripts.generators.inventory_generator import InventoryGenerator
from scripts.generators.marketing_generator import MarketingGenerator
from scripts.generators.shipment_generator import ShipmentGenerator
CustomerGenerator.generate()
ProductGenerator.generate()
InventoryGenerator.generate()
MarketingGenerator.generate()
ShipmentGenerator.generate()

def main():

    print("Generating Sample Data...\n")

    CustomerGenerator.generate()
    ProductGenerator.generate()
    InventoryGenerator.generate()
    MarketingGenerator.generate()
    ShipmentGenerator.generate()

    print("\nAll datasets generated successfully.")

if __name__ == "__main__":
    main()