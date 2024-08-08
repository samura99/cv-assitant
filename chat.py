from src.app.chat.chat import Chat
from src.utils.clean_terminal import clean

chat = Chat()
clean()

while True:
    query = input(">")
    print(f"<{chat.process_query(query)}")