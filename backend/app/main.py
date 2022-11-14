from fastapi import FastAPI
# FastAPI documentation says to use fastapi.middleware.cors, this results in errors.
from starlette.middleware.cors import CORSMiddleware
from contacts.routes import contacts_router
from contacts.check_routes import check_router
from config import config

app = FastAPI()

# Set CORS policy to allow fetch from 8080 to 8000
origins = ["http://localhost",
    "http://localhost:8080",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable /contacts endpoints
app.include_router(
    contacts_router,
    prefix="/contacts",
    tags=["contacts"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    check_router,
    prefix="/check",
    tags=["check"],
    responses={404: {"description": "Not found"}},
)


# Startup tasks
@app.on_event("startup")
async def app_startup():
   pass
    
# Shutdown tasks
@app.on_event("shutdown")
async def app_shutdown():    
    config.close_db_client()