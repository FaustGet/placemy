from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from router import authentication,ad,geocoders, files


app = FastAPI()

app.include_router(authentication.router)
app.include_router(ad.router)
app.include_router(geocoders.router)
app.include_router(files.router)




@app.middleware("http")
async def add_process(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
