import os
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates

from services.linkedin import get_jobs

from models.job_ad import *

router = APIRouter()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"test"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    password = os.environ.get("TEST_PASSWORD")
    correct_password_bytes = password.encode('utf-8')
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@router.post(
    "/process_form",
    response_model=JobAdResponse,
    name="jobs:show-jobs",
)
async def predict(
    username: Annotated[str, Depends(get_current_username)],
    location: str = Form(...),
    keywords: str = Form(...)):

    # if not data_input:
    #     raise HTTPException(status_code=404, detail="'data_input' argument invalid!")
    # try:
    #     data_point = data_input.get_np_array()
    #     prediction = get_prediction(data_point)
    #
    # except Exception as err:
    #     raise HTTPException(status_code=500, detail=f"Exception: {err}")
    jobs = get_jobs(location, keywords)
    return JobAdResponse(job_list=jobs)


@router.get(
    "/",
    name="job:get-data",
)
async def search_jobs(
        username: Annotated[str, Depends(get_current_username)],
        request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

