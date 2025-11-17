from database import supabase

def save_memory(session_id: str, key: str, value: str):
    supabase.table("memory_notes").insert({
        "session_id": session_id,
        "key": key,
        "value": value
    }).execute()


def load_memory(session_id: str):
    result = supabase.table("memory_notes") \
        .select("*") \
        .eq("session_id", session_id) \
        .execute()
    return result.data