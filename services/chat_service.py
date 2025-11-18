""" Now that the database variables are created for global accessability 
This service primarly will have functions that can be called on to power the
messaging capabilities of Brimmbot"""



from database import supabase
from datetime import datetime
from openai import OpenAI


client = OpenAI()

def save_message(session_id: str, role: str, content: str):
    
    try:
        supabase.table("messages").insert ({
            "session_id": session_id,
            "role": role,
            "content": content
        }).execute()
    except Exception as e:
        print("Error in saving_message" , e)
        raise



def get_recent_messages(session_id: str, limit: int = 10):
    
    try:
        result = supabase.table("messages") \
            .select("*") \
            .eq("session_id", session_id) \
            .order("created_at", desc=False) \
            .limit(limit) \
            .execute()
        return result.data
    except Exception as e:
        print("Error in get_recent_messages", e)
        raise


def generate_ai_response(messages: list):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content

    except Exception as e:
        print("Error in generate_ai_response", e)
        raise
