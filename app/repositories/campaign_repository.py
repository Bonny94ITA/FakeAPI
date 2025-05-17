from app.services.data_service import read_data

class CampaignRepository:
    def get_all_campaigns(self):
        return read_data().get("campaigns", [])