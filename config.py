from pydantic_settings import BaseSettings
import os
import uuid
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Settings(BaseSettings):
    PROJECT_TITLE: str = "VC Test-suite"
    PROJECT_VERSION: str = "v0"
    ALLURE_API: str = "https://allure.opsec.id/api"


settings = Settings()
