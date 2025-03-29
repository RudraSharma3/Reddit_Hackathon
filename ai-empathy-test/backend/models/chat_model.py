# backend/models/chat_model.py (Simplified for this example)
# You could define a more complex data structure to represent a chat message
# if you need to store additional information like timestamps, user IDs, etc.
# But for this basic demo, we're just using strings.

class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content