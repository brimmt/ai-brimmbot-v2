from fastapi import APIRouter
from database import supabase

router = APIRouter(prefix="/session", tags=["Session"])

@router.post("/start")
def start_session():
    try:
        # Insert new session row and return generated UUID
        result = supabase.table("sessions").insert({}).execute()
        session = result.data[0]
        return {"session_id": session["id"]}

    except Exception as e:
        print("Error creating session:", e)
        return {"error": "Failed to create session"}