from pathlib import Path
from filelock import FileLock
from fastapi import HTTPException
from .report_pipeline import ReportPipeline
import pandas as pd
import os
import httpx
import logging


logger = logging.getLogger(__name__)

class UserCampaignReportPipeline(ReportPipeline):
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "reports"))

    async def prepare(self):
        try:
            self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create '{self.REPORTS_DIR}' directory: {e}")
            raise HTTPException(status_code=500, detail="Failed to create reports directory.")

    async def fetch_data(self):
        try:
            async with httpx.AsyncClient() as client:
                users = (await client.get(f"{self.API_URL}/users")).json()
                logger.info(f"Fetched {len(users)} users.")

                transactions = (await client.get(f"{self.API_URL}/transactions")).json()
                logger.info(f"Fetched {len(transactions)} transactions.")

                campaigns = (await client.get(f"{self.API_URL}/campaigns")).json()
                logger.info(f"Fetched {len(campaigns)} campaigns.")
            return users, transactions, campaigns
        except Exception as e:
            logger.error(f"Error fetching data from API: {e}")
            raise HTTPException(status_code=500, detail="Error fetching data from API.")

    def clean_data(self, data):
        try:
            users, transactions, campaigns = data
            users_df = pd.DataFrame(users)
            transactions_df = pd.DataFrame(transactions)
            campaigns_df = pd.DataFrame(campaigns)

            # Remove users without email
            users_df = users_df[users_df['email'].notnull()]
            logger.info(f"Users after removing those without email: {len(users_df)}")

            # Normalize user names
            users_df['name'] = users_df['name'].str.title()

            return users_df, transactions_df, campaigns_df
        except Exception as e:
            logger.error(f"Error during data cleaning: {e}")
            raise HTTPException(status_code=500, detail="Error during data cleaning.")

    def aggregate_data(self, cleaned):
        try:
            users_df, transactions_df, campaigns_df = cleaned

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

            return user_campaign, campaign_revenue
        except Exception as e:
            logger.error(f"Error during data processing: {e}")
            raise HTTPException(status_code=500, detail="Error during data processing.")

    def save_reports(self, aggregated):
        try:
            user_campaign, campaign_revenue = aggregated
            user_campaign_path = self.REPORTS_DIR / "user_campaign_report.csv"
            campaign_revenue_path = self.REPORTS_DIR / "campaign_revenue_report.csv"
            
            with FileLock(str(user_campaign_path) + ".lock"):
                user_campaign.to_csv(user_campaign_path, index=False)
            with FileLock(str(campaign_revenue_path) + ".lock"):
                campaign_revenue.to_csv(campaign_revenue_path, index=False)
            logger.info("CSV reports generated successfully.")
        except Exception as e:
            logger.error(f"Error saving CSV files: {e}")
            raise HTTPException(status_code=500, detail="Error saving CSV files.")