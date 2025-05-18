from fastapi import APIRouter, Depends
from typing import List
from app.schemas.campaign import Campaign
from app.repositories.campaign_repository import get_campaign_repository, CampaignRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

get_camp = APIRouter()

@get_camp.get("/campaigns", response_model=List[Campaign])
def get_campaigns(
    campaign_repository: CampaignRepository = Depends(get_campaign_repository)
):
    logger.info("GET /campaigns called")
    return campaign_repository.get_all_campaigns()

