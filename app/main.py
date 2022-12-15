from fastapi import FastAPI

import router
from config import engine
import model

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

app.include_router(router=router.router, prefix="/api/v1", tags=["artist"])