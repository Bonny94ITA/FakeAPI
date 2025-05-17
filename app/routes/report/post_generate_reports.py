from fastapi import APIRouter, HTTPException
from app.services.user_campaign_report_pipeline import UserCampaignReportPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

gen_repo = APIRouter()

@gen_repo.post("/generate_reports")
async def generate_reports():
    logger.info("Starting report generation pipeline.")
    try:
        pipeline = UserCampaignReportPipeline()
        await pipeline.run()
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during report generation: {e}")
        raise HTTPException(status_code=500, detail="Error during report generation.")
    return {"message": "Reports generated successfully."}