from fastapi import APIRouter

from api.routes import predictor, job_ads

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(job_ads.router, tags=["job_ads"], prefix="/v1")
