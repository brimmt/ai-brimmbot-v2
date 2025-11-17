from fastapi import FastAPI
from routes.chat_router import router as chat_router
from routes.session_router import router as session_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(chat_router)
app.include_router(session_router)


@app.get("/")
def root():
    return {"message": "BrimmBot is Live!"}




