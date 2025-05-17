import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.user_campaign_report_pipeline import UserCampaignReportPipeline

@pytest.mark.asyncio
async def test_pipeline_run_calls_all_steps(monkeypatch):
    pipeline = UserCampaignReportPipeline()

    # Mock all steps
    monkeypatch.setattr(pipeline, "prepare", AsyncMock())
    monkeypatch.setattr(pipeline, "fetch_data", AsyncMock(return_value=("users", "transactions", "campaigns")))
    monkeypatch.setattr(pipeline, "clean_data", MagicMock(return_value=("users_df", "transactions_df", "campaigns_df")))
    monkeypatch.setattr(pipeline, "aggregate_data", MagicMock(return_value=("user_campaign", "campaign_revenue")))
    monkeypatch.setattr(pipeline, "save_reports", MagicMock())

    await pipeline.run()

    pipeline.prepare.assert_awaited_once()
    pipeline.fetch_data.assert_awaited_once()
    pipeline.clean_data.assert_called_once_with(("users", "transactions", "campaigns"))
    pipeline.aggregate_data.assert_called_once_with(("users_df", "transactions_df", "campaigns_df"))
    pipeline.save_reports.assert_called_once_with(("user_campaign", "campaign_revenue"))

def test_clean_data_removes_users_without_email():
    pipeline = UserCampaignReportPipeline()
    users = [
        {"id": 1, "name": "A", "email": "a@example.com"},
        {"id": 2, "name": "B", "email": None},
        {"id": 3, "name": "C", "email": "c@example.com"},
    ]
    transactions = []
    campaigns = []
    users_df, _, _ = pipeline.clean_data((users, transactions, campaigns))
    emails = set(users_df["email"])
    assert None not in emails
    assert "a@example.com" in emails
    assert "c@example.com" in emails

def test_clean_data_normalizes_names():
    pipeline = UserCampaignReportPipeline()
    users = [{"id": 1, "name": "john DOE", "email": "john@example.com"}]
    transactions = []
    campaigns = []
    users_df, _, _ = pipeline.clean_data((users, transactions, campaigns))
    assert users_df.iloc[0]["name"] == "John Doe"