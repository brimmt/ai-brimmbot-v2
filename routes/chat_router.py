from fastapi import APIRouter
from schemas.chat_schema import ChatRequestSchema
from services.chat_service import save_message, get_recent_messages,generate_ai_response
from services.memory import save_memory, load_memory
from prompts import SYSTEM_PROMPT

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/")
def chat_with_brimmbot(request: ChatRequestSchema):
    try:
       
        save_message(request.session_id, "user", request.user_input)

       
        lower_msg = request.user_input.lower()
        if "my name is" in lower_msg:
            extracted = lower_msg.split("my name is")[1].strip()
            name = extracted.split()[0].replace(".", "")
            save_memory(request.session_id, "name", name)

        memories = load_memory(request.session_id)
        memory_text = "\n".join([f"{m['key']}: {m['value']}" for m in memories])

        
        dynamic_prompt = SYSTEM_PROMPT + f"""

            Here’s what you remember about this user:
            {memory_text if memory_text else 'No stored memories yet.'}

            """

       
        history = get_recent_messages(request.session_id)

       
        bot_reply = generate_ai_response(dynamic_prompt, history)

      
        save_message(request.session_id, "assistant", bot_reply)

        return {"reply": bot_reply}

    except Exception as e:
        print("Error in /chat route:", e)
        return {"error": "BrimmBot encountered an issue. Please try again later."}


