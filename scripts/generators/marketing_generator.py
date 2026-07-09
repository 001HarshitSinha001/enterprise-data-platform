import json
import random
from datetime import datetime, timedelta
from pathlib import Path
TOTAL_CAMPAIGNS = 20

class MarketingGenerator:

    @staticmethod
    def generate():

        base_dir = Path(__file__).resolve().parents[2]

        output_file = (
            base_dir
            / "source_systems"
            / "marketing_json"
            / "marketing.json"
        )

        campaign_names = [
            "Summer Sale",
            "Winter Sale",
            "Festive Offer",
            "Mega Discount",
            "Flash Sale",
            "New Launch",
            "Weekend Offer",
            "Clearance Sale"
        ]

        channels = [
            "Facebook",
            "Instagram",
            "Google",
            "Email",
            "YouTube"
        ]

        statuses = [
            "Active",
            "Completed",
            "Scheduled"
        ]

        campaigns = []

        start_date = datetime(2026, 1, 1)

        for campaign_id in range(1, TOTAL_CAMPAIGNS + 1):

            start = start_date + timedelta(days=random.randint(0, 180))
            end = start + timedelta(days=random.randint(10, 30))

            campaigns.append({
                "campaign_id": campaign_id,
                "campaign_name": random.choice(campaign_names),
                "channel": random.choice(channels),
                "budget": random.randint(10000, 200000),
                "start_date": start.strftime("%Y-%m-%d"),
                "end_date": end.strftime("%Y-%m-%d"),
                "status": random.choice(statuses)
            })

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as file:
            json.dump(campaigns, file, indent=4)

        print("✅ Marketing data generated successfully.")