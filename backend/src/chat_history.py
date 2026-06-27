





def create_conversation(client_id: str, conversation_id: str, title: str):
    """
    Creates a new conversation.
    Called only once—the first time a message is sent in a new chat.
    """



def save_message(
    conversation_id: str,
    role: str,
    content: str,
    sources=None,
    token_usage=None):
    """
    Saves a single chat message.
    """


def get_conversation(conversation_id: str):
    """
    Returns every message in chronological order.
    """


def list_conversations(client_id: str):
    """
    Returns all conversations belonging to one browser,
    ordered by updatedAt descending.
    """