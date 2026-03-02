from .models import ChatHistory

def save_chat(db, user_message, ai_response):
    chat = ChatHistory(
        user_message=user_message,
        ai_response=ai_response
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat