from fastapi import APIRouter
from typing import List
from app.schemas.campaign import Campaign
from app.repositories.campaign_repository import CampaignRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

get_camp = APIRouter()
campaign_repository = CampaignRepository()

@get_camp.get("/campaigns", response_model=List[Campaign])
def get_campaigns():
    logger.info("GET /campaigns called")
    return campaign_repository.get_all_campaigns()

