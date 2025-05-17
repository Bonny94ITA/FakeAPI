from fastapi import APIRouter, HTTPException
from app.services.user_campaign_report_pipeline import UserCampaignReportPipeline
import traceback
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
        logger.error(f"HTTPException during report generation: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during report generation: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Unexpected error during report generation. Please check the logs for details.")
    return {"message": "Reports generated successfully."}