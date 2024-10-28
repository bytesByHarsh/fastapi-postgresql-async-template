# Built-in Dependencies
from typing import Annotated, Dict, Any
import os

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, Request, File, UploadFile
import fastapi

# Local Dependencies
# from app.core.dependencies import (
#     CurrentUser,
#     CurrentSuperUser
# )

router = fastapi.APIRouter(tags=["Users"])
