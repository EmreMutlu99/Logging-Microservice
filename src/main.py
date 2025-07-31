import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Literal
from prisma import Prisma
from dotenv import load_dotenv
from logger.logger import LoggingService
from types import SimpleNamespace
from datetime import datetime
from pytz import timezone
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()
db = Prisma()
logging_service = LoggingService(db)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


# --- Pydantic models ----

class LogRequest(BaseModel):
    service_name: str
    user_id:      int | None = None
    log_level:    Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] # Valid log levels
    message:      Optional[str] = None



class ServiceRequest(BaseModel):
    service_name: str
    is_active:    bool = True


# --- Utility / service-layer adapters ---

async def get_service_by_name(service_name: str) -> SimpleNamespace:
    # row = await db.services.find_unique It's better for unique
    row = await db.services.find_unique(
        where={ "service_name": service_name }
    )
    # row = await db.services.find_first(
    #     where={ "service_name": service_name }
    # )
    if not row:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return SimpleNamespace(
        service_id = row.service_id,
        service_name = row.service_name,
    )


# --- Endpoints ----


@app.get("/get/service")
async def get_services():
    """List all registered services."""
    return await db.services.find_many()


@app.post("/post/service")
async def create_service(req: ServiceRequest):
    """Register a new service by name."""

    existing = await db.services.find_first(where={"service_name": req.service_name})
    if existing:
        return JSONResponse(
        status_code=400,
        content={"error": f"Service '{req.service_name}' is already exist."}
        )



    await logging_service.add_service(
        service_name=req.service_name,
        is_active=req.is_active
    )
    return {"status": "success"}


@app.get("/get/log")
async def get_logs():
    return await db.log.find_many(
        include={"service": True} # log-service relation
    )


@app.post("/post/log")
async def create_log(req: LogRequest):
    svc = await get_service_by_name(req.service_name)

    if req.user_id == None:
        # 0 means log doesn't come from a user
        req.user_id = 0
    
    if req.message == None:
        req.message = "No Message"

    log = await db.log.create(
        data={
            "user_id":      req.user_id,
            "log_level":    req.log_level,
            "message":      req.message,
            "log_timestamp": datetime.now(timezone("Europe/Istanbul")),  # It's optional, because defined default in schema
            "service_id":   svc.service_id,
        }
    )
    return log

# Front-End endpoint
@app.get("/index", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join("src/frontend", "index.html")
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html bulunamadı.")
    
@app.delete("/delete/service/{service_name}")
async def delete_service(service_name: str):
    svc = await db.services.find_first(where={"service_name": service_name})
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")

    await db.log.delete_many(where={"service_id": svc.service_id})

    await db.services.delete(where={"service_id": svc.service_id})

    return {"status": "deleted"}


# <------ Optional Log Delete Endpoint ------>
# @app.delete("/delete/log/{log_id}")
# async def delete_log(log_id: int):
#     log_entry = await db.log.find_unique(where={"log_id": log_id})
#     if not log_entry:
#         raise HTTPException(status_code=404, detail="Log not found")
#
#     await db.log.delete(where={"log_id": log_id})
#     return {"status": "deleted"}


# ⚠️ WARNING: CORS is fully open (for development use only). 
# In production, restrict origins and headers for security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/frontend"), name="static")
