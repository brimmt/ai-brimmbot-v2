from fastapi import APIRouter
from schemas.chat_schema import ChatRequestSchema
from services.chat_service import save_message, get_recent_messages,generate_ai_response
from services.memory import save_memory, load_memory
from database import supabase
from prompts import SYSTEM_PROMPT

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/")
def chat_with_brimmbot(request: ChatRequestSchema):
    
    try:
        existing = (
            supabase.table("sessions")
            .select("*")
            .eq("id", request.session_id)
            .execute()
        )

        if not existing.data:
            supabase.table("sessions").insert({"id": request.session_id}).execute()

    except Exception as e:
        print("Failed to ensure session:", e)
    

    try:

       
        save_message(request.session_id, "user", request.user_input)

        lower_msg = request.user_input.lower()
        if "my name is" in lower_msg:
            extracted = lower_msg.split("my name is")[1].strip()
            name = extracted.split()[0].replace(".", "")
            save_memory(request.session_id, "name", name)

        # Load memory from DB
        memories = load_memory(request.session_id)
        memory_text = "\n".join([f"{m['key']}: {m['value']}" for m in memories]) or "No stored memories yet."

        # Build full message list for OpenAI
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Memory:\n{memory_text}"}
        ]

        # Add recent conversation history
        history = get_recent_messages(request.session_id)
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})

        # Add current user message last
        messages.append({"role": "user", "content": request.user_input})

        # Get AI reply
        bot_reply = generate_ai_response(messages)

        # Save assistant reply
        save_message(request.session_id, "assistant", bot_reply)

        return {"reply": bot_reply}

    except Exception as e:
        print("Error in /chat route:", e)
        return {"error": "BrimmBot encountered an issue. Please try again later."}


