import random
import xml.etree.ElementTree as ET
from pathlib import Path

TOTAL_SHIPMENTS = 100


class ShipmentGenerator:

    @staticmethod
    def generate():

        base_dir = Path(__file__).resolve().parents[2]

        output_file = (
            base_dir
            / "source_systems"
            / "logistics_xml"
            / "shipments.xml"
        )

        carriers = [
            "BlueDart",
            "DTDC",
            "Delhivery",
            "Ecom Express",
            "India Post"
        ]

        cities = [
            "Delhi",
            "Mumbai",
            "Pune",
            "Bangalore",
            "Hyderabad",
            "Chennai"
        ]

        statuses = [
            "Shipped",
            "In Transit",
            "Delivered",
            "Delayed"
        ]

        root = ET.Element("shipments")

        for shipment_id in range(1, TOTAL_SHIPMENTS + 1):

            shipment = ET.SubElement(root, "shipment")

            ET.SubElement(
                shipment,
                "shipment_id"
            ).text = str(shipment_id)

            ET.SubElement(
                shipment,
                "carrier"
            ).text = random.choice(carriers)

            ET.SubElement(
                shipment,
                "destination"
            ).text = random.choice(cities)

            ET.SubElement(
                shipment,
                "status"
            ).text = random.choice(statuses)

        tree = ET.ElementTree(root)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        tree.write(
            output_file,
            encoding="utf-8",
            xml_declaration=True
        )

        print("✅ Shipment data generated successfully.")