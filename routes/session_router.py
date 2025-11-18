from fastapi import APIRouter
from database import supabase

router = APIRouter(prefix="/session", tags=["Session"])

@router.post("/start")
def start_session(payload: dict):
    try:
        session_id = payload.get("session_id")
        if not session_id:
            return {"error": "session_id required"}

        # Insert session only if it doesn't already exist
        existing = supabase.table("sessions").select("*").eq("id", session_id).execute()

        if not existing.data:
            supabase.table("sessions").insert({"id": session_id}).execute()

        return {"session_id": session_id}

    except Exception as e:
        print("Error creating session:", e)
        return {"error": "Failed to create session"}