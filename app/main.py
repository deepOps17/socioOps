from fastapi import FastAPI
# from . import models
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import post, user, auth, vote

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# models.Base.metadata.create_all(bind=engine)


