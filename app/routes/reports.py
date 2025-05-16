from fastapi import APIRouter, HTTPException
from filelock import FileLock
import pandas as pd
import os
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router_2 = APIRouter()

API_URL = "http://localhost:8000"

@router_2.post("/generate_reports")
async def generate_reports():
    logger.info("Starting report generation pipeline.")

    try:
        os.makedirs("reports", exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create 'reports' directory: {e}")
        raise HTTPException(status_code=500, detail="Failed to create reports directory.")

    try:
        async with httpx.AsyncClient() as client:
            users = (await client.get(f"{API_URL}/users")).json()
            logger.info(f"Fetched {len(users)} users.")

            transactions = (await client.get(f"{API_URL}/transactions")).json()
            logger.info(f"Fetched {len(transactions)} transactions.")

            campaigns = (await client.get(f"{API_URL}/campaigns")).json()
            logger.info(f"Fetched {len(campaigns)} campaigns.")
    except Exception as e:
        logger.error(f"Error fetching data from API: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from API.")

    try:
        users_df = pd.DataFrame(users)
        transactions_df = pd.DataFrame(transactions)
        campaigns_df = pd.DataFrame(campaigns)

        # Remove users without email
        users_df = users_df[users_df['email'].notnull()]
        logger.info(f"Users after removing those without email: {len(users_df)}")

        # Normalize user names
        users_df['name'] = users_df['name'].str.title()

        # Match transactions with users and campaigns
        merged = transactions_df.merge(users_df, left_on='user_id', right_on='id', suffixes=('', '_user'))
        merged = merged.merge(campaigns_df, left_on='campaign_id', right_on='id', suffixes=('', '_campaign'))
        logger.info(f"Transactions after merging: {len(merged)}")

        # Ensure that transaction_date falls within the campaign’s start_date and end_date
        merged['date'] = pd.to_datetime(merged['date'])
        merged['start_date'] = pd.to_datetime(merged['start_date'])
        merged['end_date'] = pd.to_datetime(merged['end_date'])
        merged = merged[(merged['date'] >= merged['start_date']) & (merged['date'] <= merged['end_date'])]
        logger.info(f"Transactions after filtering by campaign dates: {len(merged)}")

        # Total spending for each user by campaign
        user_campaign = merged.groupby(['user_id', 'name', 'campaign_id', 'name_campaign'])['amount'].sum().reset_index()
        
        # Add campaign_count per user
        campaign_count = user_campaign.groupby('user_id')['campaign_id'].nunique().reset_index(name='campaign_count')
        user_campaign = user_campaign.merge(campaign_count, on='user_id')

        # Total revenue for each campaign
        campaign_revenue = merged.groupby(['campaign_id', 'name_campaign'])['amount'].sum().reset_index()
        campaign_revenue.rename(columns={'amount': 'total_revenue'}, inplace=True)
    except Exception as e:
        logger.error(f"Error during data processing: {e}")
        raise HTTPException(status_code=500, detail="Error during data processing.")

    try:
        user_campaign_path = "reports/user_campaign_report.csv"
        campaign_revenue_path = "reports/campaign_revenue_report.csv"
        with FileLock(user_campaign_path + ".lock"):
            user_campaign.to_csv(user_campaign_path, index=False)
        with FileLock(campaign_revenue_path + ".lock"):
            campaign_revenue.to_csv(campaign_revenue_path, index=False)
        logger.info("CSV reports generated successfully.")
    except Exception as e:
        logger.error(f"Error saving CSV files: {e}")
        raise HTTPException(status_code=500, detail="Error saving CSV files.")

    return {"message": "Reports generated successfully."}