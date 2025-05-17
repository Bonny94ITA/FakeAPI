from fastapi import FastAPI
from app.routes.user.get_users import get_usr
from app.routes.user.post_user import post_usr
from app.routes.transaction.get_transactions import get_tran
from app.routes.campaign.get_campaigns import get_camp
from app.routes.report.post_generate_reports import gen_repo

app = FastAPI(title="Fake API from JSON")

app.include_router(get_usr)
app.include_router(post_usr)
app.include_router(get_tran)
app.include_router(get_camp)
app.include_router(gen_repo)